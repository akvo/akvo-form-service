from django.test import TestCase
from django.test.utils import override_settings

from akvo.core_forms.models import Options


@override_settings(USE_TZ=False)
class TestFormUpdateEndpoint(TestCase):
    def test_update_form_with_updated_options(self):
        payload = {
            "id": 1693992073895,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [{
                "id": 1693992073896,
                "name": "Sit quis dapibus",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 1693992073897,
                    "order": 1,
                    "questionGroupId": 1693992073896,
                    "name": "Sit ornare commodo sit ante consectetur",
                    "type": "option",
                    "required": False,
                    "meta": False,
                    "allowOther": False,
                    "option": [{
                        "code": "NO1",
                        "name": "New Option 1",
                        "order": 1,
                        "id": 1693992338940,
                        "color": "#803838"
                    }, {
                        "code": "NO2",
                        "name": "New Option 2",
                        "order": 2,
                        "id": 1693992338941,
                        "color": "#5f5f5f"
                    }]
                }]
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
        # PUT (payload with updated options)
        payload = {
            "id": 1693992073895,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [{
                "id": 1693992073896,
                "name": "Sit quis dapibus",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 1693992073897,
                    "order": 1,
                    "questionGroupId": 1693992073896,
                    "name": "Sit ornare commodo sit ante consectetur",
                    "type": "option",
                    "required": False,
                    "meta": False,
                    "allowOther": False,
                    "option": [{
                        "code": "NO1",
                        "name": "New Option 1",
                        "order": 1,
                        "id": 1693992338940,
                        "color": "#803838"
                    }, {
                        "code": "NO3",
                        "name": "New Option 3",
                        "order": 2,
                        "id": 1693992338999,
                        "color": "#5f5f5f"
                    }]
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
            "/api/form/1693992073895",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {
            "id": 1693992073895,
            "name": "New Form",
            "description": "New Form Description",
            "defaultLanguage": "en",
            "languages": ["en"],
            "version": 1,
            "translations": None,
            "question_group": [{
                "id": 1693992073896,
                "name": "Sit quis dapibus",
                "description": None,
                "order": 1,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 1693992073897,
                    "name": "Sit ornare commodo sit ante consectetur",
                    "order": 1,
                    "type": "option",
                    "required": False,
                    "meta": False,
                    "option": [{
                        "id": 1693992338940,
                        "code": "NO1",
                        "name": "New Option 1",
                        "order": 1,
                        "color": "#803838"
                    }, {
                        "id": 1693992338999,
                        "code": "NO3",
                        "name": "New Option 3",
                        "order": 2,
                        "color": "#5f5f5f"
                    }]
                }]
            }]
        })

    def test_update_question_type_from_options_to_input(self):
        payload = {
            "id": 123,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [{
                "id": 456,
                "name": "Sit quis dapibus",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 789,
                    "order": 1,
                    "questionGroupId": 456,
                    "name": "Sit ornare commodo sit ante consectetur",
                    "type": "option",
                    "required": False,
                    "meta": False,
                    "allowOther": False,
                    "option": [{
                        "code": "NO1",
                        "name": "New Option 1",
                        "order": 1,
                        "id": 911,
                        "color": "#803838"
                    }]
                }]
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
        # PUT
        payload = {
            "id": 123,
            "name": "Update Form",
            "description": "Lorem ipsum",
            "question_group": [{
                "id": 456,
                "name": "Update Question Group",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 789,
                    "order": 1,
                    "questionGroupId": 456,
                    "name": "Update to number question",
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
            "/api/form/123",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {
            "id": 123,
            "name": "Update Form",
            "description": "Lorem ipsum",
            "defaultLanguage": "en",
            "languages": ["en"],
            "version": 1,
            "translations": None,
            "question_group": [{
                "id": 456,
                "name": "Update Question Group",
                "description": None,
                "order": 1,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 789,
                    "name": "Update to number question",
                    "order": 1,
                    "type": "number",
                    "required": False,
                    "meta": False
                }]
            }]
        })
        options = Options.objects.filter(question_id=789).all()
        self.assertEqual(len(options), 0)
