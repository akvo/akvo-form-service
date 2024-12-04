import os

from django.test import TestCase
from django.test.utils import override_settings

from akvo.core_node.models import Node

WEBDOMAIN = os.environ.get("WEBDOMAIN")


@override_settings(USE_TZ=False)
class TestMobileFormEndpoint(TestCase):
    def setUp(self):
        # POST NODE
        payload = {
            "name": "The Node",
            "node_detail": [
                {"code": "BLI", "name": "Bali"},
                {"code": "DIY", "name": "Daerah Istimewa Yogyakarta"},
            ],
        }
        data = self.client.post(
            "/api/node",
            payload,
            content_type="application/json",
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {"message": "ok"})

        self.node = Node.objects.first()

        # POST FORM
        payload = {
            "id": 1694489640833,
            "name": "New Form",
            "description": "New Form Description",
            "question_group": [
                {
                    "id": 1694489640834,
                    "name": "nam_ante_fusce",
                    "label": "Nam ante Fusce",
                    "order": 1,
                    "repeatable": False,
                    "question": [
                        {
                            "id": 1694494676197,
                            "order": 1,
                            "questionGroupId": 1694489640834,
                            "name": "augue_mauris",
                            "label": "Augue mauris tincidunt at Duis interdum",
                            "type": "input",
                            "required": False,
                            "meta": False,
                        },
                        {
                            "id": 1694489640835,
                            "order": 2,
                            "questionGroupId": 1694489640834,
                            "name": "porta_lorem_sed_ante_ac_consectetur",
                            "label": "Porta Lorem sed ante ac consectetur",
                            "type": "cascade",
                            "required": False,
                            "meta": False,
                            "api": {
                                "endpoint": f"/api/node/{self.node.id}",
                                "initial": 2,
                                "list": "children",
                            },
                        },
                    ],
                }
            ],
        }
        data = self.client.post(
            "/api/form", data=payload, content_type="application/json"
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.assertEqual(result, {"message": "ok"})

    def test_endpoint_get_mobile_form_definition(self):
        data = self.client.get(
            "/api/device/forms/1694489640833",
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        self.maxDiff = None
        self.assertEqual(
            result,
            {
                "id": 1694489640833,
                "name": "New Form",
                "description": "New Form Description",
                "defaultLanguage": "en",
                "languages": ["en"],
                "version": 1,
                "cascades": [f"{WEBDOMAIN}/sqlite/the_node.sqlite"],
                "translations": None,
                "question_group": [
                    {
                        "name": "nam_ante_fusce",
                        "label": "Nam ante Fusce",
                        "description": None,
                        "order": 1,
                        "repeatable": False,
                        "translations": None,
                        "repeat_text": None,
                        "question": [
                            {
                                "id": 1694494676197,
                                "name": "augue_mauris",
                                "label": "Augue mauris tincidunt at Duis interdum",
                                "order": 1,
                                "type": "input",
                                "required": False,
                                "meta": False,
                                "display_only": False,
                                "required_double_entry": False,
                            },
                            {
                                "id": 1694489640835,
                                "name": "porta_lorem_sed_ante_ac_consectetur",
                                "label": "Porta Lorem sed ante ac consectetur",
                                "order": 2,
                                "type": "cascade",
                                "required": False,
                                "meta": False,
                                "display_only": False,
                                "api": {
                                    "list": "children",
                                    "initial": 2,
                                    "endpoint": f"/api/node/{self.node.id}",
                                },
                                "source": {"file": "the_node.sqlite", "parent_id": 0},
                                "required_double_entry": False,
                            },
                        ],
                    }
                ],
            },
        )
