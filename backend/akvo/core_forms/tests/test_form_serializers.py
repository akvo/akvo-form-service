import json

from django.test import TestCase
from rest_framework.test import APIClient
from akvo.core_forms.models import Forms
from akvo.core_forms.serializers.form import (
    ListFormSerializer,
    AddFormSerializer
)


class TestFormSerializers(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "name": "Test Form",
            "description": "Lorem ipsum sit dolor",
            "version": 1,
            "languages": ["en"],
            "default_language": "en",
            "translations": None,
        }
        self.instance = Forms.objects.create(**self.data)
        self.serializer = ListFormSerializer(instance=self.instance)

    def test_list_form_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {
                "id", "name", "description", "defaultLanguage",
                "version", "languages", "translations",
            },
        )

    def test_list_form_serializer_return_expected_data(self):
        data = self.serializer.data
        expected_data = {
            "id": data.get("id"),
            "name": "Test Form",
            "description": "Lorem ipsum sit dolor",
            "version": 1,
            "languages": ["en"],
            "defaultLanguage": "en",
            "translations": None,
        }
        self.assertEqual(data, expected_data)

    def test_add_form_serializer_valid(self):
        expected_payload = {}
        # Load expected form payload
        with open('./source/static/example_form_payload.json', 'r') as f:
            expected_payload = json.load(f)
        serializer = AddFormSerializer(data=expected_payload)
        self.assertEqual(expected_payload, expected_payload)
        self.assertTrue(serializer.is_valid())
