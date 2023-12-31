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
                "question": [payload_question[0]] + [{
                    "id": 1693987349188,
                    "order": 2,
                    "questionGroupId": 1693987349171,
                    "name": "Add new number question",
                    "type": "number",
                    "required": False,
                    "meta": False
                }]
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
                    "id": 1693987349172,
                    "name": "Phasellus amet suscipit ac tristique nisl",
                    "order": 1,
                    "type": "input",
                    "required": False,
                    "meta": False
                }, {
                    "id": 1693987349188,
                    "name": "Add new number question",
                    "order": 2,
                    "type": "number",
                    "required": False,
                    "meta": False
                }]
            }]
        })

    def test_endpoint_put_form_with_deleted_question_group(self):
        payload_question_group = [{
            "id": 1693988922938,
            "name": "Ante aliquet lorem",
            "order": 1,
            "repeatable": False,
            "question": [{
                "id": 1693988922939,
                "order": 1,
                "questionGroupId": 1693988922938,
                "name": "Dolor ante augue adipiscing elit amet",
                "type": "input",
                "required": False,
                "meta": False
            }]
        }, {
            "id": 1693988928051,
            "name": "Consequat Donec neque",
            "order": 2,
            "repeatable": False,
            "question": [{
                "id": 1693988928052,
                "order": 1,
                "questionGroupId": 1693988928051,
                "name": "Ornare consectetur neque Donec nisl lorem",
                "type": "input",
                "required": False,
                "meta": False
            }]
        }]
        payload = {
            "id": 1693988922937,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": payload_question_group
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
        # PUT (payload with question group removed)
        payload = {
            "id": 1693988922937,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [payload_question_group[0]] + [{
                "id": 1693988922977,
                "name": "New Question Group",
                "order": 2,
                "repeatable": False,
                "question": [{
                    "id": 1693988922955,
                    "order": 1,
                    "questionGroupId": 1693988922977,
                    "name": "New Question",
                    "type": "number",
                    "required": False,
                    "meta": False
                }]
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
            "/api/form/1693988922937",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {
            "id": 1693988922937,
            "name": "New Form",
            "description": "New Form Description",
            "defaultLanguage": "en",
            "languages": ["en"],
            "version": 1,
            "translations": None,
            "question_group": [{
                "id": 1693988922938,
                "name": "Ante aliquet lorem",
                "description": None,
                "order": 1,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 1693988922939,
                    "name": "Dolor ante augue adipiscing elit amet",
                    "order": 1,
                    "type": "input",
                    "required": False,
                    "meta": False
                }]
            }, {
                "id": 1693988922977,
                "name": "New Question Group",
                "description": None,
                "order": 2,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 1693988922955,
                    "name": "New Question",
                    "order": 1,
                    "type": "number",
                    "required": False,
                    "meta": False
                }]
            }]
        })

    def test_form_definition_return_disableDelete_param_if_has_answers(self):
        payload = {
            "id": 1694509989310,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [{
                "id": 1694509989312,
                "name": "Dapibus lorem ultrices",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 1694509989313,
                    "order": 1,
                    "questionGroupId": 1694509989312,
                    "name": "Augue neque sapien ultrices eu quis",
                    "type": "input",
                    "required": False,
                    "meta": False
                }]
            }]
        }
        data = self.client.post(
            "/api/form",
            data=payload,
            content_type="application/json"
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {"message": "ok"})
        # post answer
        answer_payload = {
            "data": {
                "name": "Testing Data",
                "geo": None,
                "submitter": "Akvo",
            },
            "answer": [{
                "question": 1694509989313,
                "value": "Test answer"
            }],
        }
        data = self.client.post(
            f"/api/data/{payload.get('id')}",
            answer_payload,
            content_type="application/json",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {"message": "ok"})
        # get form after post
        data = self.client.get(
            f"/api/form/{payload.get('id')}",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {
            "id": 1694509989310,
            "name": "New Form",
            "description": "New Form Description",
            "defaultLanguage": "en",
            "languages": ["en"],
            "version": 1,
            "translations": None,
            "question_group": [{
                "id": 1694509989312,
                "name": "Dapibus lorem ultrices",
                "description": None,
                "order": 1,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 1694509989313,
                    "name": "Augue neque sapien ultrices eu quis",
                    "order": 1,
                    "type": "input",
                    "required": False,
                    "meta": False,
                    "disableDelete": True
                }]
            }]
        })
