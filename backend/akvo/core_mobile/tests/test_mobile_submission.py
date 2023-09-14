# We are using the same serializer for mobile submission and web submission
# This test is to make sure that the mobile submission is working as expected

import datetime
from django.test import TestCase
from django.test.utils import override_settings
from django.core.management import call_command
from akvo.core_data.models import Data, Answers
from akvo.core_mobile.serializers.mobile_form import (
    MobileFormSubmissionSerializer,
)


@override_settings(USE_TZ=False)
class TestMobileFormSubmission(TestCase):
    def setUp(self):
        call_command("form_seeder", "--file=./source/forms/1693403249322.json")
        self.payload = {
            "formId": "1693403249322",
            "name": "Data 1",
            "duration": 20,
            "submittedAt": "2021-06-01 00:00:00",
            "submitter": "Jane",
            "geo": [0, 0],
            "answers": {
                "1693403277316": "Farm 1",
                "1693403399692": 20,
                "1693403503687": ["KG"],
                "1693403547388": 20,
                "1693403843111": 20,
                "1693403947085": ["Acre"],
                "1693404048281": 20,
                "1693403971287": 20,
            },
        }

    def test_mobile_submission_serializer(self):
        data = MobileFormSubmissionSerializer(data=self.payload)
        self.assertTrue(data.is_valid())
        internal_data = data.to_internal_value(self.payload)
        self.assertEqual(
            internal_data.get("data"),
            {
                "name": "Data 1",
                "geo": [0, 0],
                "submitter": "Jane",
                "duration": 20,
            },
        )
        self.assertEqual(internal_data.get("formId"), 1693403249322)
        self.assertEqual(internal_data.get("name"), "Data 1")
        self.assertEqual(internal_data.get("duration"), 20)
        self.assertEqual(
            internal_data.get("submittedAt"), datetime.datetime(2021, 6, 1, 0, 0)
        )
        self.assertEqual(internal_data.get("submitter"), "Jane")
        self.assertEqual(internal_data.get("geo"), [0, 0])
        self.assertEqual(
            internal_data.get("answer"),
            [
                {"question": "1693403277316", "value": "Farm 1"},
                {"question": "1693403399692", "value": 20},
                {"question": "1693403503687", "value": ["KG"]},
                {"question": "1693403547388", "value": 20},
                {"question": "1693403843111", "value": 20},
                {"question": "1693403947085", "value": ["Acre"]},
                {"question": "1693404048281", "value": 20},
                {"question": "1693403971287", "value": 20},
            ],
        )

    def test_mobile_form_submission(self):
        response = self.client.post(
            "/api/device/sync",
            self.payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "ok")
        data = Data.objects.filter(form_id=1693403249322).first()
        self.assertEqual(data.form_id, 1693403249322)
        self.assertEqual(data.name, "Data 1")
        self.assertEqual(data.submitter, "Jane")
        answers = Answers.objects.filter(data=data)
        self.assertEqual(answers.count(), 8)
