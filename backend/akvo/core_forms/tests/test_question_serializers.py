from django.test import TestCase
from rest_framework.test import APIClient
from akvo.core_forms.models import Forms, QuestionGroups, Questions
from akvo.core_forms.constants import QuestionTypes
from akvo.core_forms.serializers.question_group import (
    ListQuestionGroupSerializer
)
from akvo.core_forms.serializers.question import (
    ListQuestionSerializer
)


class TestQuestionGroupSerializers(TestCase):
    def setUp(self):
        self.client = APIClient()
        form_data = {
            "name": "Test Form",
            "description": "Lorem ipsum sit dolor",
            "version": 1,
            "languages": ["en"],
            "default_language": "en",
            "translations": None,
        }
        self.form = Forms.objects.create(**form_data)
        question_group_data = {
            "form": self.form,
            "name": "Group 1",
            "description": "Lorem ipsum sit dolor",
            "order": 1,
            "repeatable": False,
            "translations": None,
        }
        self.question_group = QuestionGroups.objects.create(
            **question_group_data
        )
        self.data = {
            "form": self.form,
            "question_group": self.question_group,
            "name": "Name",
            "order": 1,
            "type": QuestionTypes.input,
            "tooltip": "Lorem ipsum",
            "required": True,
            "meta": True,
            "rule": None,
            "dependency": None,
            "api": None,
            "extra": None,
            "autofield": None,
            "translations": None,
        }
        self.instance = Questions.objects.create(**self.data)
        self.serializer = ListQuestionSerializer(instance=self.instance)
        self.question_group_serializer = ListQuestionGroupSerializer(
            instance=self.question_group
        )

    def test_list_question_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {"id", "name", "order", "type", "tooltip", "required", "meta"},
        )

    def test_list_question_serializer_return_expected_data(self):
        data = self.serializer.data
        expected_data = {
            "id": data.get("id"),
            "name": "Name",
            "order": 1,
            "type": QuestionTypes.FieldStr.get(QuestionTypes.input),
            "tooltip": "Lorem ipsum",
            "required": True,
            "meta": True,
        }
        self.assertEqual(data, expected_data)

    def test_list_question_group_serializer_return_question(self):
        question_data = self.serializer.data
        question_group_data = self.question_group_serializer.data
        expected_data = {
            "id": question_group_data.get("id"),
            "name": "Group 1",
            "description": "Lorem ipsum sit dolor",
            "order": 1,
            "repeatable": False,
            "translations": None,
            "question": [question_data],
        }
        self.assertEqual(question_group_data, expected_data)
