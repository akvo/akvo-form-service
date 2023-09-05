from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from akvo.core_forms.models import QuestionGroups
from akvo.core_forms.serializers.question import (
    ListQuestionSerializer,
    AddQuestionSerializer
)
from akvo.utils.custom_serializer_fields import (
    CustomIntegerField,
    CustomListField,
    CustomCharField,
    CustomBooleanField
)


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


class AddQuestionGroupSerializer(serializers.ModelSerializer):
    id = CustomIntegerField()
    name = CustomCharField()
    description = CustomCharField(required=False, allow_null=True)
    order = CustomIntegerField()
    repeatable = CustomBooleanField(
        required=False, allow_null=True, default=False)
    translations = CustomListField(required=False, allow_null=True)
    question = AddQuestionSerializer(many=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = QuestionGroups
        fields = [
            "id",
            "name",
            "description",
            "order",
            "repeatable",
            "translations",
            "question"
        ]
