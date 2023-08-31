from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from akvo.core_forms.models import Forms, QuestionGroups
from akvo.core_forms.serializers.question_group import (
    ListQuestionGroupSerializer
)


class ListFormSerializer(serializers.ModelSerializer):
    question_group = serializers.SerializerMethodField()

    @extend_schema_field(ListQuestionGroupSerializer(many=True))
    def get_question_group(self, instance: QuestionGroups):
        return ListQuestionGroupSerializer(
            instance=instance.question_groups.all().order_by("order"),
            many=True,
        ).data

    class Meta:
        model = Forms
        fields = [
            "id",
            "name",
            "description",
            "default_language",
            "languages",
            "version",
            "translations",
            "question_group"
        ]
