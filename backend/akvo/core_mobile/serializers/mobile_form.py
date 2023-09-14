import os

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from akvo.core_forms.models import Forms, Questions, QuestionGroups
from akvo.core_forms.serializers.question import ListQuestionSerializer
from akvo.core_forms.constants import QuestionTypes
from akvo.utils.functions import get_node_sqlite_source

WEBDOMAIN = os.environ.get("WEBDOMAIN")


class ListMobileQuestionGroupSerializer(serializers.ModelSerializer):
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
            "name",
            "description",
            "order",
            "repeatable",
            "translations",
            "question",
        ]


class MobileFormDefinitionSerializer(serializers.ModelSerializer):
    defaultLanguage = serializers.SerializerMethodField()
    cascades = serializers.SerializerMethodField()
    question_group = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_defaultLanguage(self, instance: Forms):
        return instance.default_language

    @extend_schema_field(serializers.ListField())
    def get_cascades(self, instance: Forms):
        cascade_questions = Questions.objects.filter(
            type=QuestionTypes.cascade, form=instance
        ).all()
        source = []
        for cascade_question in cascade_questions:
            # get node name from api endpoint
            cascade_url = cascade_question.api.get("endpoint", None)
            source_file = get_node_sqlite_source(cascade_url=cascade_url)
            if not source_file:
                continue
            source.append(f"{WEBDOMAIN}/sqlite/{source_file}")
        return source

    @extend_schema_field(ListMobileQuestionGroupSerializer(many=True))
    def get_question_group(self, instance: Forms):
        return ListMobileQuestionGroupSerializer(
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
            "cascades",
            "translations",
            "question_group",
        ]


class MobileFormSubmissionRequestSerializer(serializers.Serializer):
    # MobileFormSubmissionSerializer is used for validation only
    formId = serializers.IntegerField()
    name = serializers.CharField()
    duration = serializers.IntegerField()
    submittedAt = serializers.DateTimeField()
    submitter = serializers.CharField()
    geo = serializers.ListField(child=serializers.IntegerField(), required=False)
    answers = serializers.DictField()


class MobileFormSubmissionSerializer(serializers.Serializer):
    formId = serializers.IntegerField()
    name = serializers.CharField()
    duration = serializers.IntegerField()
    submittedAt = serializers.DateTimeField()
    submitter = serializers.CharField()
    geo = serializers.ListField(child=serializers.IntegerField(), required=False)
    answers = serializers.DictField()
    answer = serializers.ListField(child=serializers.DictField())
    data = serializers.DictField()

    def validate(self, data):
        if not data.get("answers"):
            raise serializers.ValidationError("Answers is required.")
        return data

    def validate_formId(self, value):
        form = Forms.objects.filter(id=value).first()
        if not form:
            raise serializers.ValidationError("Form not found.")
        return value

    def to_internal_value(self, submission):
        answers = []
        qna = submission.get("answers")
        for q in list(qna):
            answers.append({"question": q, "value": qna[q]})
        submission["answer"] = answers
        submission["data"] = {
            "name": submission.get("name"),
            "geo": submission.get("geo"),
            "submitter": submission.get("submitter"),
            "duration": submission.get("duration"),
        }
        return super().to_internal_value(submission)
