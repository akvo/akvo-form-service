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
from akvo.utils.custom_serializer_fields import validate_serializers_message


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


class AddFormSerializer(serializers.Serializer):
    id = CustomIntegerField()
    name = CustomCharField()
    description = CustomCharField(required=False, allow_null=True)
    default_language = CustomCharField(
        required=False, allow_null=True, default="en")
    languages = CustomListField(
        required=False, allow_null=True, default=["en"])
    version = CustomIntegerField(
        required=False, allow_null=True, default=1)
    translations = CustomListField(required=False, allow_null=True)
    question_group = AddQuestionGroupSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        # Get the value
        default_language = kwargs.pop('defaultLanguage', None)
        super(AddFormSerializer, self).__init__(*args, **kwargs)
        # Set the value
        if default_language:
            self.fields['default_language'].initial = default_language

    def validate_question_group(self, value):
        serializer = AddQuestionGroupSerializer(data=value, many=True)
        if not serializer.is_valid():
            print('QG ERROR', serializer.errors)
            raise serializers.ValidationError({
                "message": validate_serializers_message(serializer.errors),
                "details": serializer.errors,
            })
        return value

    def create(self, validated_data):
        question_groups_data = validated_data.pop("question_group", [])
        form = Forms.objects.create(**validated_data)
        for qg in question_groups_data:
            serializer = AddQuestionGroupSerializer(data=qg)
            if not serializer.is_valid():
                raise serializers.ValidationError({
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                })
            serializer.save(form=form)
            return object
        return form

    # class Meta:
    #     model = Forms
    #     fields = [
    #         "id",
    #         "name",
    #         "description",
    #         "default_language",
    #         "languages",
    #         "version",
    #         "translations",
    #     ]
