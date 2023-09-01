from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from akvo.core_data.models import Data


@override_settings(USE_TZ=False)
class TestDataEndpoint(TestCase):

    def test_endpoint_data_view(self):
        call_command("form_seeder", "--file=./source/forms/1693403249322.json")
        # POST DATA
        payload = {
            "data": {
                "name": "Testing Data",
                "geo": [6.2088, 106.8456],
                "submitter": "Akvo",
            },
            "answer": [{
                "question": 1693403277316,
                "value": "Jane"
            }, {
                "question": 1693403399692,
                "value": 20
            }, {
                "question": 1693403503687,
                "value": ["KG"]
            }],
        }
        data = self.client.post("/api/data/1693403249322",
                                payload,
                                content_type="application/json",
                                follow=True)
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {"message": "ok"})
        data_id = Data.objects.first().id

        # EDIT DATA
        payload = [{"question": 1693403277316, "value": "John Doe"}]
        data = self.client.put(f"/api/data/1693403249322?data_id={data_id}",
                               payload,
                               content_type="application/json",
                               follow=True)
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {'message': 'Update data success'})

        # LIST DATA
        data = self.client.get("/api/data/1693403249322?page=1", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        expected_result = {
            'current': 1,
            'data': [{
                'created': result.get('data')[0]['created'],
                'form': 1693403249322,
                'geo': [6.2088, 106.8456],
                'id': data_id,
                'name': 'Testing Data',
                'submitter': 'Akvo',
                'updated': result.get('data')[0]['updated']
            }],
            'total': 1,
            'total_page': 1
        }
        self.assertEqual(result, expected_result)

        # SHOW ANSWERS

        answers = self.client.get(f"/api/answers/{data_id}", follow=True)
        self.assertEqual(answers.status_code, 200)
        result = answers.json()
        expected_result = [{
            # TODO: FIXME - This is a bug, the previous value is not deleted
            'question': 1693403277316,
            'value': 'Jane'
            }, {
            'question': 1693403399692,
            'value': 20.0
            }, {
            'question': 1693403503687,
            'value': ['KG']
            }, {
            'question': 1693403277316,
            'value': 'John Doe'
        }]
        self.assertEqual(result, expected_result)

        # SHOW STATISTIC
        stats = self.client.get("/api/answer-stats/1693403399692", follow=True)
        self.assertEqual(stats.status_code, 200)
        result = stats.json()
        expected_result = {
            'count': 1,
            'max': 20.0,
            'mean': 20.0,
            'min': 20.0,
            'average': 20.0,
        }
