from django.test import TestCase
from rest_framework.test import APIClient
from akvo.core_forms.models import Forms, QuestionGroups, Questions
from akvo.core_forms.constants import QuestionTypes
from akvo.core_data.serializers.data import (
    SubmitDataSerializer,
    # SubmitFormSerializer,
    # ListDataSerializer
)
# from akvo.core_data.serializers.answer import (
#     SubmitDataAnswerSerializer,
#     ListAnswerSerializer
# )


class TestDataAndAnswerSerializers(TestCase):
    def setUp(self):
        self.client = APIClient()
        form_data = {
            "name": "Test Form",
            "description": "Lorem ipsum sit dolor",
            "version": 1,
            "languages": ["en"],
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
        self.question_group = QuestionGroups.objects.create(**question_group_data)
        question_data = {
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
        self.question = Questions.objects.create(**question_data)

    def test_submit_data_serializer_validation(self):
        post_data = {
            'name': 'John',
            'geo': {'lat': 40.7128, 'lng': -74.0060},
            'submitter': 'Akvo'
        }
        serializer = SubmitDataSerializer(**post_data)
        self.assertTrue(serializer.is_valid())
