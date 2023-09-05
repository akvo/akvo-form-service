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
from akvo.utils.custom_serializer_fields import validate_serializers_message


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
    form = CustomIntegerField(read_only=True)
    id = CustomIntegerField()
    name = CustomCharField()
    description = CustomCharField(required=False, allow_null=True)
    order = CustomIntegerField()
    repeatable = CustomBooleanField(
        required=False, allow_null=True, default=False)
    translations = CustomListField(required=False, allow_null=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create(self, validated_data):
        questions_data = validated_data.pop("question", [])
        qg = QuestionGroups.objects.create(**validated_data)
        for q in questions_data:
            q["form"] = validated_data.get("form")
            q["question_group"] = qg
            serializer = AddQuestionSerializer(data=q)
            if not serializer.is_valid():
                raise serializers.ValidationError({
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                })
            serializer.save()
            return object
        return qg

    class Meta:
        model = QuestionGroups
        fields = [
            "id",
            "name",
            "description",
            "order",
            "repeatable",
            "translations",
        ]
