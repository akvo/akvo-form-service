from django.utils import timezone

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
    OpenApiParameter,
)
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from akvo.core_data.models import Data, Answers
from akvo.core_data.serializers.data import (
    SubmitFormSerializer,
    ListDataSerializer
)
from akvo.core_data.serializers.answer import (
    SubmitDataAnswerSerializer
)
from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.models import Forms, Questions
from akvo.utils.custom_serializer_fields import validate_serializers_message
from akvo.utils.default_serializers import DefaultResponseSerializer
from akvo.utils.custom_pagination import Pagination


class DataView(APIView):
    @extend_schema(
        responses={
            (200, "application/json"): inline_serializer(
                "DataList",
                fields={
                    "current": serializers.IntegerField(),
                    "total": serializers.IntegerField(),
                    "total_page": serializers.IntegerField(),
                    "data": ListDataSerializer(many=True),
                },
            )
        },
        tags=["Data"],
        parameters=[
            OpenApiParameter(
                name="page",
                required=True,
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
            )
        ],
        summary="To get list of form data",
    )
    def get(self, request, form_id):
        form = get_object_or_404(Forms, pk=form_id)
        queryset = form.data.order_by("-updated", "-created")
        paginator = Pagination()
        instance = paginator.paginate_queryset(queryset, request)
        # Serialize the paginated queryset and return it in the response
        serializer = ListDataSerializer(instance=instance, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=SubmitFormSerializer,
        responses={200: DefaultResponseSerializer},
        tags=["Data"],
        summary="Submit form data",
    )
    def post(self, request, form_id):
        form = get_object_or_404(Forms, pk=form_id)
        serializer = SubmitFormSerializer(
            data=request.data, context={"form": form}
        )
        if not serializer.is_valid():
            return Response(
                {
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

    @extend_schema(
        request=SubmitDataAnswerSerializer(many=True),
        responses={200: DefaultResponseSerializer},
        tags=["Data"],
        parameters=[
            OpenApiParameter(
                name="data_id",
                required=True,
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
            )
        ],
        summary="Edit form data",
    )
    def put(self, request, form_id):
        data_id = request.GET["data_id"]
        get_object_or_404(Forms, pk=form_id)
        data = get_object_or_404(Data, pk=data_id)
        serializer = SubmitDataAnswerSerializer(
            data=request.data, many=True
        )
        if not serializer.is_valid():
            return Response(
                {
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        answers = request.data
        for answer in answers:
            question_id = answer.get("question")
            question = Questions.objects.get(id=question_id)
            form_answer = Answers.objects.filter(
                data=data, question_id=question_id
            ).first()
            name = None
            value = None
            option = None
            if question.type in [
                QuestionTypes.geo,
                QuestionTypes.option,
                QuestionTypes.multiple_option,
            ]:
                option = answer.get("value")
            elif question.type in [
                QuestionTypes.input,
                QuestionTypes.text,
                QuestionTypes.photo,
                QuestionTypes.date,
            ]:
                name = answer.get("value")
            else:
                # for number question type
                value = answer.get("value")
            # Update answer
            form_answer.data = data
            form_answer.question = question
            form_answer.name = name
            form_answer.value = value
            form_answer.options = option
            form_answer.updated = timezone.now()
            form_answer.save()
        # update datapoint
        data.updated = timezone.now()
        data.save()
        return Response(
            {"message": "Update data success"}, status=status.HTTP_200_OK
        )
