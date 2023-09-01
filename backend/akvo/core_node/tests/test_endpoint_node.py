from django.test import TestCase
from django.test.utils import override_settings
from akvo.core_node.models import Node


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
        )
        self.assertEqual(data.status_code, 200)
        data = data.json()
        self.assertEqual(data, {"message": "ok"})
        node_id = Node.objects.first().id

        # GET LIST OF NODE DETAIL
        data = self.client.get(
            f"/api/node_detail/{node_id}",
            follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        expected_result = [
            {'id': 1, 'code': 'JKT', 'name': 'Jakarta'},
            {'id': 2, 'code': 'DPS', 'name': 'Denpasar'},
            {'id': 3, 'code': 'DIY', 'name': 'Daerah Istimewa Yogyakarta'}
        ]
        self.assertEqual(result, expected_result)
