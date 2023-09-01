import json

from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(USE_TZ=False)
class TestFormEndpoint(TestCase):
    def test_endpoint_list_form(self):
        call_command("form_seeder", "--file=./source/forms/1693403249322.json")
        data = self.client.get(
            "/api/forms",
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        expected_result = [{
            'id': 1693403249322,
            'name': 'IDH Form',
            'description': 'IDH Yield value proof of concept',
            'defaultLanguage': 'en',
            'languages': ['en'],
            'version': 1,
            'translations': None
        }]
        self.assertEqual(result, expected_result)

    def test_endpoint_get_form_by_id(self):
        call_command("form_seeder", "--file=./source/forms/1693403249322.json")
        data = self.client.get(
            "/api/form/1693403249322",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        # Load expected form definition from JSON
        with open('./source/static/expected_form_definition.json', 'r') as f:
            expected_result = json.load(f)
        self.assertEqual(result, expected_result)
