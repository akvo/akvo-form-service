from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from akvo.core_data.models import Answers
from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.models import Questions
from akvo.utils.custom_serializer_fields import (
    CustomPrimaryKeyRelatedField,
    UnvalidatedField,
)
from akvo.utils.functions import get_answer_value


class SubmitDataAnswerSerializer(serializers.ModelSerializer):
    value = UnvalidatedField(allow_null=False)
    question = CustomPrimaryKeyRelatedField(queryset=Questions.objects.none())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields.get("question").queryset = Questions.objects.all()

    def validate_value(self, value):
        return value

    def validate(self, attrs):
        value = attrs.get("value")
        question_type = attrs.get("question").type
        question_id = attrs.get("question").id

        def raise_validation_error(message):
            raise serializers.ValidationError(
                f"{message} for Question:{question_id}"
            )

        if value == "" or (isinstance(value, list) and len(value) == 0):
            raise_validation_error("Value is required")

        if question_type in [
            QuestionTypes.geo,
            QuestionTypes.option,
            QuestionTypes.multiple_option,
        ]:
            if not isinstance(value, list):
                raise_validation_error("Valid list value is required")
        elif question_type in [
            QuestionTypes.input,
            QuestionTypes.text,
            QuestionTypes.photo,
            QuestionTypes.date,
        ]:
            if not isinstance(value, str):
                raise_validation_error("Valid string value is required")
        elif question_type in [QuestionTypes.number, QuestionTypes.cascade]:
            if not (isinstance(value, int) or isinstance(value, float)):
                raise_validation_error("Valid number value is required")

        return attrs

    class Meta:
        model = Answers
        fields = ["question", "value"]


class ListAnswerSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.ANY)
    def get_value(self, instance: Answers):
        return get_answer_value(instance)

    class Meta:
        model = Answers
        fields = ["question", "value"]
