from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
    OpenApiParameter,
)
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from akvo.core_data.models import Answers
from django.db.models import Min, Max, Sum, Count


@extend_schema(
    responses={
        (200, "application/json"): inline_serializer(
            "StatsAnswer",
            fields={
                "min": serializers.FloatField(),
                "max": serializers.FloatField(),
                "total": serializers.FloatField(),
                "count": serializers.FloatField(),
            },
        )
    },
    tags=["Data"],
    summary="To get list of form data",
)
@api_view(["GET"])
def answer_stats(request, question_id):
    instance = Answers.objects.filter(question_id=question_id).all()
    if not instance:
        return Response(status=status.HTTP_404_NOT_FOUND)
    min = instance.aggregate(min=Min("value"))["min"]
    max = instance.aggregate(max=Max("value"))["max"]
    total = instance.aggregate(total=Sum("value"))["total"]
    count = instance.aggregate(count=Count("value"))["count"]
    return Response(
        {"min": min, "max": max, "total": total, "count": count},
        status=status.HTTP_200_OK,
    )
