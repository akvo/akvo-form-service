from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from akvo.core_forms.models import (
    Forms,
    QuestionGroups,
    Questions
)
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
from akvo.core_data.models import Answers


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
    def get_question_group(self, instance: Forms):
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
        return form

    def update(self, instance, validated_data):
        # update form
        instance.name = validated_data.get(
            'name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.version = validated_data.get(
            'version', instance.version)
        instance.languages = validated_data.get(
            'languages', instance.languages)
        instance.default_language = validated_data.get(
            'default_language', instance.default_language)
        instance.translations = validated_data.get(
            'translations', instance.translations)

        # check and delete question group
        current_qgs = QuestionGroups.objects.filter(form=instance).all()
        current_qg_ids = [cqg.id for cqg in current_qgs]

        new_qg_data = validated_data.get('question_group', [])
        new_qg_ids = [nqg.get('id') for nqg in new_qg_data]

        # create or update question group
        for qg in new_qg_data:
            current_qg = QuestionGroups.objects.filter(id=qg.get('id')).first()
            serializer = AddQuestionGroupSerializer(data=qg)
            if not serializer.is_valid():
                raise serializers.ValidationError({
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                })
            if not current_qg:
                serializer.save(form=instance)
            if current_qg:
                serializer.update(
                    instance=current_qg,
                    validated_data=serializer.validated_data)

        missing_qg_ids = list(set(current_qg_ids) - set(new_qg_ids))
        # delete missing question groups
        for qgid in missing_qg_ids:
            questions = Questions.objects.filter(question_group_id=qgid).all()
            qids = [q.id for q in questions]
            # check answers
            answers = Answers.objects.filter(question_id__in=qids).count()
            if answers:
                raise serializers.ValidationError({
                    "message": "Can't delete question group",
                    "details": f"Question in group {qgid} has answers",
                })
            QuestionGroups.objects.filter(id=qgid).delete()
        instance.save()
        return instance
