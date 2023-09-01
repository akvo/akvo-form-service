from drf_spectacular.utils import (
    extend_schema, )
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from akvo.core_data.models import Answers
from akvo.core_data.serializers.answer import (
    ListAnswerSerializer, )


class AnswerView(APIView):

    @extend_schema(
        responses={(200, "application/json"): ListAnswerSerializer(many=True)},
        tags=["Data"],
        summary="To get list of answers",
    )
    def get(self, _, data_id):
        instance = Answers.objects.filter(data_id=data_id).all()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ListAnswerSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
