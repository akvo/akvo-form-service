from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from akvo.core_forms.models import Forms
from akvo.core_data.models import (
    Data,
    Answers,
)
from akvo.utils.custom_serializer_fields import (
    CustomCharField,
)
from akvo.utils.functions import update_date_time_format
from akvo.core_data.serializers.answer import (
    SubmitDataAnswerSerializer
)


class SubmitDataSerializer(serializers.ModelSerializer):
    submitter = CustomCharField(allow_null=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields.get("form").queryset = Forms.objects.all()

    def validate_submitter(self, value):
        if not value or value == "":
            raise serializers.ValidationError("Submitter is required")
        return value

    class Meta:
        model = Data
        fields = ["form", "name", "geo", "submitter"]


class SubmitFormSerializer(serializers.Serializer):
    data = SubmitDataSerializer()
    answer = SubmitDataAnswerSerializer(many=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        data = validated_data.get("data")
        obj_data = self.fields.get("data").create(data)
        for answer in validated_data.get("answer"):
            Answers.objects.define_answer_value(
                data=obj_data,
                answer=answer
            )
        return object


class ListDataSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_created(self, instance: Data):
        return update_date_time_format(instance.created)

    @extend_schema_field(OpenApiTypes.STR)
    def get_updated(self, instance: Data):
        return update_date_time_format(instance.updated)

    class Meta:
        model = Data
        fields = [
            "id",
            "name",
            "form",
            "geo",
            "submitter",
            "created",
            "updated",
        ]
