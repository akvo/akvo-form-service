from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from akvo.core_forms.models import Forms
from akvo.core_forms.serializers.form import (
    ListFormSerializer,
    FormDefinitionSerializer,
    AddFormSerializer,
)
from akvo.utils.default_serializers import DefaultResponseSerializer
from akvo.utils.custom_serializer_fields import validate_serializers_message


@extend_schema(
    responses={
        200: ListFormSerializer(many=True)
    },
    tags=['Form'],
    summary='To get list of forms',
    description='Get list of all forms')
@api_view(['GET'])
def list_form(request):
    instance = Forms.objects.all()
    return Response(
        ListFormSerializer(instance=instance, many=True).data,
        status=status.HTTP_200_OK
    )


@extend_schema(
    responses={
        200: FormDefinitionSerializer()
    },
    tags=['Form'],
    summary='To get a form definition by form id',
    description='Get form definition by form id')
@api_view(['GET'])
def get_form_by_id(request, form_id):
    instance = get_object_or_404(Forms, pk=form_id)
    return Response(
        FormDefinitionSerializer(instance=instance).data,
        status=status.HTTP_200_OK
    )


class FormManagementView(APIView):
    @extend_schema(
        request=AddFormSerializer(),
        responses={
            (200, "application/json"): DefaultResponseSerializer,
        },
        tags=["Form"],
        summary="Create form definition",
    )
    def post(self, request):
        serializer = AddFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(
            {"message": "ok"}, status=status.HTTP_200_OK
        )

    @extend_schema(
        request=AddFormSerializer(),
        responses={
            (200, "application/json"): DefaultResponseSerializer,
        },
        tags=["Form"],
        summary="Update form definition",
    )
    def put(self, request):
        form_id = request.data.get('id')
        instance = get_object_or_404(Forms, pk=form_id)
        serializer = AddFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.update(
            instance=instance, validated_data=serializer.validated_data)
        return Response(
            {"message": "Update form success"}, status=status.HTTP_200_OK
        )
