from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from akvo.core_forms.models import Forms, Questions
from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.serializers.question_group import (
    ListQuestionGroupSerializer
)
from akvo.utils.functions import get_node_sqlite_source


class MobileFormDefinitionSerializer(serializers.ModelSerializer):
    cascades = serializers.SerializerMethodField()
    question_group = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField())
    def get_cascades(self, instance: Forms):
        cascade_questions = Questions.objects.filter(
            type=QuestionTypes.cascade, form=instance).all()
        source = []
        for cascade_question in cascade_questions:
            # get node name from api endpoint
            cascade_url = cascade_question.api.get("endpoint", None)
            source_file = get_node_sqlite_source(cascade_url=cascade_url)
            if not source_file:
                continue
            source.append(f"/sqlite/{source_file}")
        return source

    @extend_schema_field(ListQuestionGroupSerializer(many=True))
    def get_question_group(self, instance: Forms):
        return ListQuestionGroupSerializer(
            instance=instance.question_groups.all().order_by("order"),
            many=True,
        ).data

    class Meta:
        model = Forms
        fields = [
            'name', 'version', 'cascades',
            'question_group', 'translations'
        ]
