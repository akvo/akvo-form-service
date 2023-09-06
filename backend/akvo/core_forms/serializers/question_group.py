from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from akvo.core_forms.models import QuestionGroups, Questions
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
from akvo.core_data.models import Answers


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
        return qg

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.order = validated_data.get(
            'order', instance.order)
        instance.repeatable = validated_data.get(
            'repeatable', instance.repeatable)
        instance.translations = validated_data.get(
            'translations', instance.translations)

        # check and delete question
        current_qs = Questions.objects.filter(question_group=instance).all()
        current_qs_ids = [cq.id for cq in current_qs]

        new_q_data = validated_data.get('question', [])
        new_q_ids = [nq.get('id') for nq in new_q_data]
        missing_q_ids = list(set(current_qs_ids) - set(new_q_ids))
        print('MISSING QG IDS', missing_q_ids)
        # check missing question ids with answer and delete
        for qid in missing_q_ids:
            answers = Answers.objects.filter(question_id=qid).count()
            if not answers:
                Questions.objects.filter(id=qid).delete()

        # create or update questions
        for q in new_q_data:
            current_q = Questions.objects.filter(id=q.get('id')).first()
            serializer = AddQuestionSerializer(data=q)
            if not serializer.is_valid():
                raise serializers.ValidationError({
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                })
            if not current_q:
                serializer.save(
                    form=instance.form, question_group=instance)
            if current_q:
                serializer.update(
                    instance=current_q,
                    validated_data=serializer.validated_data)

        return instance
