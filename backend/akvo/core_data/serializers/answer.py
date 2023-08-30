from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from akvo.core_data.models import Answers
from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.models import Questions
from akvo.utils.custom_serializer_fields import (
    CustomPrimaryKeyRelatedField,
    UnvalidatedField,
)
from utils.functions import get_answer_value


class SubmitDataAnswerSerializer(serializers.ModelSerializer):
    value = UnvalidatedField(allow_null=False)
    question = CustomPrimaryKeyRelatedField(queryset=Questions.objects.none())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields.get("question").queryset = Questions.objects.all()

    def validate_value(self, value):
        return value

    def validate(self, attrs):
        if attrs.get("value") == "":
            raise ValidationError(
                "Value is required for Question:{0}".format(attrs.get("question").id)
            )

        if isinstance(attrs.get("value"), list) and len(attrs.get("value")) == 0:
            raise ValidationError(
                "Value is required for Question:{0}".format(attrs.get("question").id)
            )

        if not isinstance(attrs.get("value"), list) and attrs.get("question").type in [
            QuestionTypes.geo,
            QuestionTypes.option,
            QuestionTypes.multiple_option,
        ]:
            raise ValidationError(
                "Valid list value is required for Question:{0}".format(
                    attrs.get("question").id
                )
            )
        elif not isinstance(attrs.get("value"), str) and attrs.get("question").type in [
            QuestionTypes.input,
            QuestionTypes.text,
            QuestionTypes.photo,
            QuestionTypes.date,
        ]:
            raise ValidationError(
                "Valid string value is required for Question:{0}".format(
                    attrs.get("question").id
                )
            )
        elif not (
            isinstance(attrs.get("value"), int) or isinstance(attrs.get("value"), float)
        ) and attrs.get("question").type in [
            QuestionTypes.number,
            QuestionTypes.cascade,
        ]:
            raise ValidationError(
                "Valid number value is required for Question:{0}".format(
                    attrs.get("question").id
                )
            )
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
