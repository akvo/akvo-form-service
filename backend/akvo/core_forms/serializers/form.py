from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from akvo.core_forms.models import Forms, QuestionGroups
from akvo.core_forms.serializers.question_group import (
    ListQuestionGroupSerializer,
    AddQuestionGroupSerializer
)
from akvo.utils.custom_serializer_fields import (
    CustomIntegerField,
    CustomCharField,
    CustomListField
)


class ListFormSerializer(serializers.ModelSerializer):
    defaultLanguage = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_defaultLanguage(self, instance: Forms):
        return instance.default_language

    class Meta:
        model = Forms
        fields = [
            "id",
            "name",
            "description",
            "defaultLanguage",
            "languages",
            "version",
            "translations",
        ]


class FormDefinitionSerializer(serializers.ModelSerializer):
    defaultLanguage = serializers.SerializerMethodField()
    question_group = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_defaultLanguage(self, instance: Forms):
        return instance.default_language

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
            "defaultLanguage",
            "languages",
            "version",
            "translations",
            "question_group"
        ]


class AddFormSerializer(serializers.ModelSerializer):
    id = CustomIntegerField()
    name = CustomCharField()
    description = CustomCharField(required=False, allow_null=True)
    default_language = CustomCharField(
        required=False, allow_null=True,
        default="en", source="defaultLanguage")
    languages = CustomListField(
        required=False, allow_null=True, default=["en"])
    version = CustomIntegerField(
        required=False, allow_null=True, default=1)
    translations = CustomListField(required=False, allow_null=True)
    question_group = AddQuestionGroupSerializer(many=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
