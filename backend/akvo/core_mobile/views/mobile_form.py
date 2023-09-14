from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from akvo.core_forms.models import Forms
from akvo.core_data.serializers.data import SubmitFormSerializer
from akvo.core_mobile.serializers.mobile_form import (
    MobileFormDefinitionSerializer,
    MobileFormSubmissionSerializer,
)
from akvo.utils.custom_serializer_fields import validate_serializers_message
from akvo.utils.default_serializers import DefaultResponseSerializer


@extend_schema(
    responses={200: MobileFormDefinitionSerializer},
    tags=["Mobile Device Form"],
    summary="To get form in mobile form format by form id",
)
@api_view(["GET"])
def get_mobile_form_definition(request, form_id):
    instance = get_object_or_404(Forms, id=form_id)
    instance = MobileFormDefinitionSerializer(instance=instance).data
    return Response(instance, status=status.HTTP_200_OK)


@extend_schema(
    request=MobileFormSubmissionSerializer,
    responses={200: DefaultResponseSerializer},
    tags=["Mobile Device Form"],
    summary="Submit mobile form data",
)
@api_view(["POST"])
def sync_form_data(request):
    form = get_object_or_404(Forms, pk=request.data.get("formId"))
    if not request.data.get("answers"):
        return Response(
            {"message": "Answers is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    data = MobileFormSubmissionSerializer(data=request.data)
    if not data.is_valid():
        return Response(
            {
                "message": validate_serializers_message(data.errors),
                "details": data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    data = data.to_internal_value(data.validated_data)
    serializer = SubmitFormSerializer(data=data, context={"form": form})
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
