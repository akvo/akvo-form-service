from django.test import TestCase
from rest_framework.test import APIClient
from akvo.core_forms.models import Forms, QuestionGroups
from akvo.core_forms.serializers import ListQuestionGroupSerializer


class TestQuestionGroupSerializers(TestCase):
    def setUp(self):
        self.client = APIClient()
        form_data = {
            'name': 'Test Form',
            'description': 'Lorem ipsum sit dolor',
            'version': 1,
            'languages': ['en'],
            'translations': None
        }
        self.form = Forms.objects.create(**form_data)
        self.data = {
            'form': self.form,
            'name': 'Group 1',
            'description': 'Lorem ipsum sit dolor',
            'order': 1,
            'repeatable': False,
            'translations': None
        }
        self.instance = QuestionGroups.objects.create(**self.data)
        self.serializer = ListQuestionGroupSerializer(instance=self.instance)

    def test_list_question_group_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()), 
            {
                'id', 'name', 'description', 
                'order', 'repeatable', 'translations',
                'question'
            }
        )

    def test_list_question_group_serializer_return_expected_data(self):
        data = self.serializer.data
        expected_data = {
            'id': data.get('id'),
            'name': 'Group 1',
            'description': 'Lorem ipsum sit dolor',
            'order': 1,
            'repeatable': False,
            'translations': None,
            'question': []
        }
        self.assertEqual(data, expected_data)
