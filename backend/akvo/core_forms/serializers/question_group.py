from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from akvo.core_forms.models import QuestionGroups
from akvo.core_forms.serializers.question import ListQuestionSerializer


class ListQuestionGroupSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    @extend_schema_field(ListQuestionSerializer(many=True))
    def get_question(self, instance: QuestionGroups):
        return ListQuestionSerializer(
            instance=instance.question_group_questions.all().order_by("order"),
            many=True,
        ).data

    class Meta:
        model = QuestionGroups
        fields = [
            "id",
            "name",
            "description",
            "order",
            "repeatable",
            "translations",
            "question",
        ]
