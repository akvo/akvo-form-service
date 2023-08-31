from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from akvo.core_forms.models import Forms
from akvo.core_forms.serializers.form import ListFormSerializer


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
