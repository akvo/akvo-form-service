from django.test import TestCase
from django.test.utils import override_settings


@override_settings(USE_TZ=False)
class TestNodeEndpoint(TestCase):
    def test_endpoint_node_view(self):
        # POST DATA
        payload = {
            "name": "Example Node",
            "node_detail": [
                {"code": "JKT", "name": "Jakarta"},
                {"code": "DPS", "name": "Denpasar"},
                {"code": "DIY", "name": "Daerah Istimewa Yogyakarta"},
            ],
        }
        data = self.client.post(
            "/api/node",
            payload,
            content_type="application/json",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {"message": "ok"})
