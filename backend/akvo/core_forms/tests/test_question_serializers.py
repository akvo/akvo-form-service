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
from akvo.core_forms.serializers.form import (
    FormDefinitionSerializer
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
            "name": "group_1",
            "label": "Group 1",
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
            "name": "name",
            "label": "Name",
            "order": 1,
            "type": QuestionTypes.input,
            "tooltip": "Lorem ipsum",
            "required": True,
            "meta": True,
            "display_only": False,
            "rule": None,
            "dependency": None,
            "api": None,
            "extra": None,
            "autofield": None,
            "translations": None,
            "pre": None,
        }
        self.instance = Questions.objects.create(**self.data)
        self.serializer = ListQuestionSerializer(instance=self.instance)
        self.question_group_serializer = ListQuestionGroupSerializer(
            instance=self.question_group
        )
        self.form_serializer = FormDefinitionSerializer(instance=self.form)

    def test_list_question_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {
                "id",
                "name",
                "label",
                "order",
                "type",
                "tooltip",
                "required",
                "meta",
                "display_only",
            },
        )

    def test_list_question_serializer_return_expected_data(self):
        data = self.serializer.data
        expected_data = {
            "id": data.get("id"),
            "name": "name",
            "label": "Name",
            "order": 1,
            "type": QuestionTypes.FieldStr.get(QuestionTypes.input),
            "tooltip": "Lorem ipsum",
            "required": True,
            "meta": True,
            "display_only": False,
        }
        self.assertEqual(data, expected_data)

    def test_list_question_group_serializer_return_question(self):
        question_data = self.serializer.data
        question_group_data = self.question_group_serializer.data
        expected_data = {
            "id": question_group_data.get("id"),
            "name": "group_1",
            "label": "Group 1",
            "description": "Lorem ipsum sit dolor",
            "order": 1,
            "repeatable": False,
            "translations": None,
            "question": [question_data],
        }
        self.assertEqual(question_group_data, expected_data)

    def test_form_definition_serializer_return_question_group(self):
        question_group_data = self.question_group_serializer.data
        form_data = self.form_serializer.data
        expected_data = {
            "id": form_data.get("id"),
            "name": "Test Form",
            "description": "Lorem ipsum sit dolor",
            "version": 1,
            "languages": ["en"],
            "defaultLanguage": "en",
            "translations": None,
            "question_group": [question_group_data]
        }
        self.assertEqual(form_data, expected_data)
