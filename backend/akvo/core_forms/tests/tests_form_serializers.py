from django.test import TestCase
from rest_framework.test import APIClient
from akvo.core_forms.models import Forms
from akvo.core_forms.serializers import ListFormSerializer


class TestFormSerializers(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            'name': 'Test Form',
            'description': 'Lorem ipsum sit dolor',
            'version': 1,
            'languages': ['en'],
            'translations': None
        }
        self.instance = Forms.objects.create(**self.data)
        self.serializer = ListFormSerializer(instance=self.instance)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()), 
            {
                'id', 'name', 'description', 
                'version', 'languages', 'translations'
            }
        )
