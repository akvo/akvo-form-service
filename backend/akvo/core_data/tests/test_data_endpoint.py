from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(USE_TZ=False)
class TestDataEndpoint(TestCase):
    def test_endpoint_data_view(self):
        call_command("form_seeder", "--file=1693403249322")
        # POST DATA
        payload = {
            "data": {
                "name": "Testing Data",
                "geo": [6.2088, 106.8456],
                "submitter": "Akvo",
            },
            "answer": [
                {"question": 1693403277316, "value": "Jane"},
                {"question": 1693403399692, "value": 20},
                {"question": 1693403503687, "value": ["KG"]},
            ],
        }
        data = self.client.post(
            "/api/data/1693403249322",
            payload,
            content_type="application/json",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {"message": "ok"})

        # EDIT DATA
        payload = [
            {"question": 1693403277316, "value": "John Doe"},
        ]
        data = self.client.put(
            "/api/data/1693403249322?data_id=1",
            payload,
            content_type="application/json",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {'message': 'Update data success'})

        # LIST DATA
        data = self.client.get(
            "/api/data/1693403249322?page=1",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        expected_result = {
            'current': 1,
            'data': [{
                'created': result.get('data')[0]['created'],
                'form': 1693403249322,
                'geo': [6.2088, 106.8456],
                'id': 1,
                'name': 'Testing Data',
                'submitter': 'Akvo',
                'updated': result.get('data')[0]['updated']
            }],
            'total': 1,
            'total_page': 1
        }
        self.assertEqual(result, expected_result)