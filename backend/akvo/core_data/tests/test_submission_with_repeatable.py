from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from akvo.core_data.models import Data
from akvo.core_forms.models import Forms


@override_settings(USE_TZ=False)
class TestSubmissionWithRepeatAnswers(TestCase):
    def setUp(self) -> None:
        call_command(
            "form_seeder",
            "--file=./source/forms/test_form_with_repeatable.json")
        self.form = Forms.objects.first()
        # POST DATA
        payload = {
            "data": {
                "name": "Testing Data with repeat answers",
                "geo": None,
                "submitter": "Akvo",
            },
            "answer": [{
                "question": 1694745892380,
                "value": "Jane"
            }, {
                "question": 1694745902446,
                "value": 20
            }, {
                "question": 1694745925476,
                "value": "Repeat 1",
                "repeat": 0,
            }, {
                "question": 1694746018883,
                "value": 12,
                "repeat": 0,
            }, {
                "question": 1694745925476,
                "value": "Repeat 2",
                "repeat": 1,
            }, {
                "question": 1694746018883,
                "value": 22,
                "repeat": 1,
            }],
        }
        data = self.client.post(
            f"/api/data/{self.form.id}",
            payload,
            content_type="application/json",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {"message": "ok"})
        self.data = Data.objects.first()

    def test_add_submission_with_repeatable(self):
        # LIST DATA
        data = self.client.get(f"/api/data/{self.form.id}?page=1", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        expected_result = {
            'current': 1,
            'data': [{
                'created': result.get('data')[0]['created'],
                'form': self.form.id,
                'geo': None,
                'id': self.data.id,
                'name': 'Testing Data with repeat answers',
                'submitter': 'Akvo',
                'updated': None
            }],
            'total': 1,
            'total_page': 1
        }
        self.assertEqual(result, expected_result)

        # SHOW ANSWERS
        answers = self.client.get(f"/api/answers/{self.data.id}", follow=True)
        self.assertEqual(answers.status_code, 200)
        result = answers.json()
        expected_result = [{
            "question": 1694745892380,
            "value": "Jane",
            "repeat": 0
        }, {
            "question": 1694745902446,
            "value": 20.0,
            "repeat": 0
        }, {
            "question": 1694745925476,
            "value": "Repeat 1",
            "repeat": 0
        }, {
            "question": 1694746018883,
            "value": 12.0,
            "repeat": 0
        }, {
            "question": 1694745925476,
            "value": "Repeat 2",
            "repeat": 1
        }, {
            "question": 1694746018883,
            "value": 22.0,
            "repeat": 1
        }]
        self.assertEqual(result, expected_result)

    def test_update_submission_with_repeatable(self):
        # EDIT DATA
        payload = [{
            "question": 1694745892380,
            "value": "John Doe"
        }, {
            "question": 1694745902446,
            "value": 10
        }, {
            "question": 1694745925476,
            "value": "Repeat 2",
            "repeat": 0,
        }, {
            "question": 1694746018883,
            "value": 5,
            "repeat": 0,
        }, {
            "question": 1694745925476,
            "value": "Repeat 3",
            "repeat": 1,
        }, {
            "question": 1694746018883,
            "value": 9,
            "repeat": 1,
        }]
        data = self.client.put(
            f"/api/data/{self.form.id}?data_id={self.data.id}",
            payload,
            content_type="application/json",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {'message': 'Update data success'})

        # SHOW ANSWERS
        answers = self.client.get(f"/api/answers/{self.data.id}", follow=True)
        self.assertEqual(answers.status_code, 200)
        result = answers.json()
        expected_result = [{
            "question": 1694745892380,
            "value": "John Doe",
            "repeat": 0
        }, {
            "question": 1694745902446,
            "value": 10.0,
            "repeat": 0
        }, {
            "question": 1694745925476,
            "value": "Repeat 2",
            "repeat": 0
        }, {
            "question": 1694746018883,
            "value": 5.0,
            "repeat": 0
        }, {
            "question": 1694745925476,
            "value": "Repeat 3",
            "repeat": 1
        }, {
            "question": 1694746018883,
            "value": 9.0,
            "repeat": 1
        }]
        self.assertEqual(result, expected_result)
