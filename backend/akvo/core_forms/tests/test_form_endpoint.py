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

    def test_endpoint_post_form(self):
        with open('./source/static/example_form_payload.json', 'r') as f:
            expected_payload = json.load(f)
        data = self.client.post(
            "/api/form",
            data=expected_payload,
            content_type="application/json"
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {"message": "ok"})
        # get form after post
        data = self.client.get(
            f"/api/form/{expected_payload.get('id')}",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        with open(
            './source/static/example_form_payload_result.json', 'r'
        ) as f:
            expected_result = json.load(f)
        self.assertEqual(result, expected_result)

    def test_endpoint_put_form_with_deleted_question(self):
        payload_question = [{
            "id": 1693987349172,
            "order": 1,
            "questionGroupId": 1693987349171,
            "name": "Phasellus amet suscipit ac tristique nisl",
            "type": "input",
            "required": False,
            "meta": False
        }, {
            "id": 1693987361547,
            "order": 2,
            "questionGroupId": 1693987349171,
            "name": "Tincidunt mauris tristique eu dapibus augue",
            "type": "input",
            "required": False,
            "meta": False
        }]
        payload = {
            "id": 1693987349170,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [{
                "id": 1693987349171,
                "name": "Lorem lorem Nam",
                "order": 1,
                "repeatable": False,
                "question": payload_question
            }]
        }
        # POST
        data = self.client.post(
            "/api/form",
            data=payload,
            content_type="application/json"
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {"message": "ok"})
        # PUT (payload with question removed)
        payload = {
            "id": 1693987349170,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [{
                "id": 1693987349171,
                "name": "Lorem lorem Nam",
                "order": 1,
                "repeatable": False,
                "question": [payload_question[1]]
            }]
        }
        data = self.client.put(
            "/api/form",
            data=payload,
            content_type="application/json"
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {"message": "Update form success"})
        # GET
        data = self.client.get(
            "/api/form/1693987349170",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {
            "id": 1693987349170,
            "name": "New Form",
            "description": "New Form Description",
            "defaultLanguage": "en",
            "languages": ["en"],
            "version": 1,
            "translations": None,
            "question_group": [{
                "id": 1693987349171,
                "name": "Lorem lorem Nam",
                "description": None,
                "order": 1,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 1693987361547,
                    "name": "Tincidunt mauris tristique eu dapibus augue",
                    "order": 2,
                    "type": "input",
                    "required": False,
                    "meta": False
                }]
            }]
        })
