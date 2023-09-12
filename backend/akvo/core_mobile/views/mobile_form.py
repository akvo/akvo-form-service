from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from akvo.core_forms.models import Forms
from akvo.core_mobile.serializers.mobile_form import (
    MobileFormDefinitionSerializer
)


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
