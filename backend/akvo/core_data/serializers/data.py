import requests
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from akvo.core_data.models import (
    Data,
    Answers,
)
from akvo.core_forms.constants import QuestionTypes
from akvo.utils.custom_serializer_fields import (
    CustomCharField,
)
from akvo.utils.functions import update_date_time_format
from akvo.core_data.serializers.answer import (
    SubmitDataAnswerSerializer
)


class SubmitDataSerializer(serializers.ModelSerializer):
    submitter = CustomCharField(allow_null=False)

    def validate_submitter(self, value):
        if not value or value == "":
            raise serializers.ValidationError("Submitter is required")
        return value

    class Meta:
        model = Data
        fields = ["name", "geo", "submitter"]


class SubmitFormSerializer(serializers.Serializer):
    data = SubmitDataSerializer()
    answer = SubmitDataAnswerSerializer(many=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        data = validated_data.get("data")
        data["form"] = self.context.get("form")
        obj_data = self.fields.get("data").create(data)

        for answer in validated_data.get("answer"):
            name = None
            value = None
            option = None

            if answer.get("question").type in [
                QuestionTypes.geo,
                QuestionTypes.option,
                QuestionTypes.multiple_option,
            ]:
                option = answer.get("value")
            elif answer.get("question").type in [
                QuestionTypes.input,
                QuestionTypes.text,
                QuestionTypes.photo,
                QuestionTypes.date,
            ]:
                name = answer.get("value")
            elif answer.get("question").type == QuestionTypes.cascade:
                val = None
                id = answer.get("value")
                ep = answer.get("question").api.get("endpoint")
                ep = ep.split("?")[0]
                ep = f"{ep}?id={id}"
                val = requests.get(ep).json()
                val = val[0].get("name")
                name = val
            else:
                # for number question type
                value = answer.get("value")

            Answers.objects.create(
                data=obj_data,
                question=answer.get("question"),
                name=name,
                value=value,
                options=option,
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
