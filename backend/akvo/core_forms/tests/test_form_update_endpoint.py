from django.test import TestCase
from django.test.utils import override_settings

from akvo.core_forms.models import Options


@override_settings(USE_TZ=False)
class TestFormUpdateEndpoint(TestCase):
    def test_post_data(self):
        payload = {
            "id": 1695287858303,
            "name": "New Form",
            "description": "New Form Description",
            "languages": ["en", "af"],
            "defaultLanguage": "af",
            "question_group": [{
                "id": 1695287858304,
                "name": "eu_augue_consectetur",
                "label": "Eu augue consectetur",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 1695287858305,
                    "order": 1,
                    "questionGroupId": 1695287858304,
                    "name": "amet_lorem_porta_at_suscipit_facilisis",
                    "label": "Amet lorem porta at suscipit facilisis",
                    "type": "autofield",
                    "required": False,
                    "meta": False,
                    "dataApiUrl": "test.com",
                    "fn": {
                        "multiline": False,
                        "fnString": "() => console.log('test')",
                        "fnColor": {}
                    }
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
        # GET
        data = self.client.get(
            "/api/form/1695287858303",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {
            "id": 1695287858303,
            "name": "New Form",
            "description": "New Form Description",
            "defaultLanguage": "af",
            "languages": ["en", "af"],
            "version": 1,
            "translations": None,
            "question_group": [{
                "id": 1695287858304,
                "name": "eu_augue_consectetur",
                "label": "Eu augue consectetur",
                "description": None,
                "order": 1,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 1695287858305,
                    "name": "amet_lorem_porta_at_suscipit_facilisis",
                    "label": "Amet lorem porta at suscipit facilisis",
                    "order": 1,
                    "type": "autofield",
                    "required": False,
                    "meta": False,
                    "display_only": False,
                    "fn": {
                        "fnColor": {},
                        "fnString": "() => console.log('test')",
                        "multiline": False
                    },
                    "dataApiUrl": "test.com",
                    "required_double_entry": False,
                }],
                "repeat_text": None,
            }]
        })

    def test_update_form_with_updated_options(self):
        payload = {
            "id": 1693992073895,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [{
                "id": 1693992073896,
                "name": "sit_quis_dapibus",
                "label": "Sit quis dapibus",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 1693992073897,
                    "order": 1,
                    "questionGroupId": 1693992073896,
                    "name": "sit_ornare_commodo_sit_ante_consectetur",
                    "label": "Sit ornare commodo sit ante consectetur",
                    "type": "option",
                    "required": False,
                    "meta": False,
                    "allowOther": False,
                    "option": [{
                        "label": "New Option 1",
                        "value": "new_option_1",
                        "order": 1,
                        "id": 1693992338940,
                        "color": "#803838"
                    }, {
                        "label": "New Option 2",
                        "value": "new_option_2",
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
                "name": "sit_quis_dapibus",
                "label": "Sit quis dapibus",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 1693992073897,
                    "order": 1,
                    "questionGroupId": 1693992073896,
                    "name": "sit_ornare_commodo_sit_ante_consectetur",
                    "label": "Sit ornare commodo sit ante consectetur",
                    "type": "option",
                    "required": False,
                    "meta": False,
                    "allowOther": False,
                    "dataApiUrl": "https://jsonplaceholder.typicode.com/todos/1",
                    "option": [{
                        "label": "New Option 1",
                        "value": "new_option_1",
                        "order": 1,
                        "id": 1693992338940,
                        "color": "#803838"
                    }, {
                        "label": "New Option 3",
                        "value": "new_option_3",
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
                "name": "sit_quis_dapibus",
                "label": "Sit quis dapibus",
                "description": None,
                "order": 1,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 1693992073897,
                    "name": "sit_ornare_commodo_sit_ante_consectetur",
                    "label": "Sit ornare commodo sit ante consectetur",
                    "order": 1,
                    "type": "option",
                    "required": False,
                    "meta": False,
                    "display_only": False,
                    "dataApiUrl": "https://jsonplaceholder.typicode.com/todos/1",
                    "option": [{
                        "id": 1693992338940,
                        "label": "New Option 1",
                        "value": "new_option_1",
                        "order": 1,
                        "color": "#803838"
                    }, {
                        "id": 1693992338999,
                        "label": "New Option 3",
                        "value": "new_option_3",
                        "order": 2,
                        "color": "#5f5f5f"
                    }],
                    "required_double_entry": False,
                }],
                "repeat_text": None,
            }]
        })

    def test_update_question_type_from_options_to_input(self):
        payload = {
            "id": 123,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [{
                "id": 456,
                "name": "sit_quis_dapibus",
                "label": "Sit quis dapibus",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 789,
                    "order": 1,
                    "questionGroupId": 456,
                    "name": "sit_ornare_commodo_sit_ante_consectetur",
                    "label": "Sit ornare commodo sit ante consectetur",
                    "type": "option",
                    "required": False,
                    "meta": False,
                    "allowOther": False,
                    "option": [{
                        "label": "New Option 1",
                        "value": "new_option_1",
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
                "name": "update_question_group",
                "label": "Update Question Group",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 789,
                    "order": 1,
                    "questionGroupId": 456,
                    "name": "update_to_number_question",
                    "label": "Update to number question",
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
                "name": "update_question_group",
                "label": "Sit quis dapibus",
                "description": None,
                "order": 1,
                "repeatable": False,
                "translations": None,
                "question": [{
                    "id": 789,
                    "name": "update_to_number_question",
                    "label": "Update to number question",
                    "order": 1,
                    "type": "number",
                    "required": False,
                    "meta": False,
                    "display_only": False,
                    "required_double_entry": False,
                }],
                "repeat_text": None,
            }]
        })
        options = Options.objects.filter(question_id=789).all()
        self.assertEqual(len(options), 0)

    def test_update_question_which_has_answers(self):
        payload = {
            "id": 123,
            "name": "Form",
            "description": "Lorem ipsum..",
            "question_group": [{
                "id": 456,
                "name": "question_group_1",
                "label": "Question Group 1",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 789,
                    "order": 1,
                    "questionGroupId": 456,
                    "name": "your_name",
                    "label": "Your Name",
                    "type": "input",
                    "required": False,
                    "meta": False,
                }]
            }]
        }
        # POST FORM
        data = self.client.post(
            "/api/form",
            data=payload,
            content_type="application/json"
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {"message": "ok"})
        # POST DATA
        payload = {
            "data": {
                "name": "Testing Data",
                "geo": None,
                "submitter": "Akvo",
            },
            "answer": [{
                "question": 789,
                "value": "Jane"
            }],
        }
        data = self.client.post(
            "/api/data/123",
            payload,
            content_type="application/json",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {"message": "ok"})
        # PUT - Update Form change question type should error
        payload = {
            "id": 123,
            "name": "Update Form",
            "description": "Lorem ipsum",
            "question_group": [{
                "id": 456,
                "name": "update_question_group",
                "label": "Update Question Group",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 789,
                    "order": 1,
                    "questionGroupId": 456,
                    "name": "update_to_number_question",
                    "label": "Update to number question",
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
        self.assertEqual(data.status_code, 400)
        result = data.json()
        self.assertEqual(
            result,
            {
                'message': "Can't update question type",
                'details': 'Question 789 has answers'
            }
        )
        # PUT - Update Form delete question should error
        payload = {
            "id": 123,
            "name": "Update Form",
            "description": "Lorem ipsum",
            "question_group": [{
                "id": 456,
                "name": "update_question_group",
                "label": "Update Question Group",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 987,
                    "order": 1,
                    "questionGroupId": 456,
                    "name": "new_question",
                    "label": "New Question",
                    "type": "input",
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
        self.assertEqual(data.status_code, 400)
        result = data.json()
        self.assertEqual(
            result,
            {
                'message': "Can't delete question",
                'details': 'Question 789 has answers'
            }
        )
        # PUT - Update Form delete question group should error
        payload = {
            "id": 123,
            "name": "Update Form",
            "description": "Lorem ipsum",
            "question_group": [{
                "id": 654,
                "name": "new_question_group",
                "label": "New Question Group",
                "order": 1,
                "repeatable": False,
                "question": [{
                    "id": 999,
                    "order": 1,
                    "questionGroupId": 456,
                    "name": "new_question",
                    "label": "New Question",
                    "type": "input",
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
        self.assertEqual(data.status_code, 400)
        result = data.json()
        self.assertEqual(
            result,
            {
                'message': "Can't delete question group",
                'details': 'Question in group 456 has answers'
            }
        )
