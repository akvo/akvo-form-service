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


class AddQuestionGroupSerializer(serializers.Serializer):
    form = CustomIntegerField(read_only=True)
    id = CustomIntegerField()
    name = CustomCharField()
    description = CustomCharField(required=False, allow_null=True)
    order = CustomIntegerField()
    repeatable = CustomBooleanField(
        required=False, allow_null=True, default=False)
    translations = CustomListField(required=False, allow_null=True)
    question = AddQuestionSerializer(many=True)

    def __init__(self, *args, **kwargs):
        # Get the value
        form = kwargs.pop('form', None)
        super(AddQuestionGroupSerializer, self).__init__(*args, **kwargs)
        # Set the value
        if form:
            self.fields['form'].initial = form

    def validate_question(self, value):
        serializer = AddQuestionSerializer(data=value, many=True)
        if not serializer.is_valid():
            print('Q ERROR', serializer.errors)
            raise serializers.ValidationError({
                "message": validate_serializers_message(serializer.errors),
                "details": serializer.errors,
            })
        return value

    def create(self, validated_data):
        questions_data = validated_data.pop("question", [])
        qg = QuestionGroups.objects.create(**validated_data)
        for q in questions_data:
            serializer = AddQuestionSerializer(data=q)
            if not serializer.is_valid():
                raise serializers.ValidationError({
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                })
            serializer.save(form=qg.form, question_group=qg)
            return object
        return qg

    # class Meta:
    #     model = QuestionGroups
    #     fields = [
    #         "id",
    #         "name",
    #         "description",
    #         "order",
    #         "repeatable",
    #         "translations",
    #     ]
