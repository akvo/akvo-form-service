import os
from django.test import TestCase
from django.test.utils import override_settings
from akvo.core_node.models import Node, NodeDetail
import pandas as pd


@override_settings(USE_TZ=False)
class TestNodeEndpoint(TestCase):
    def test_endpoint_node_view(self):
        # POST DATA
        payload = {
            "name": "Example Node",
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
        node_id = Node.objects.first().id

        # GET LIST OF NODE DETAIL
        data = self.client.get(f"/api/node-detail/{node_id}", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        bali_id = NodeDetail.objects.get(name="Bali").id
        yogya_id = NodeDetail.objects.get(name="Daerah Istimewa Yogyakarta").id
        expected_result = [
            {"id": bali_id, "code": "BLI", "name": "Bali", "parent_id": None},
            {
                "id": yogya_id,
                "code": "DIY",
                "name": "Daerah Istimewa Yogyakarta",
                "parent_id": None,
            },
        ]
        self.assertEqual(result, expected_result)

        # POST WITH PARENT

        payload = {
            "name": "Example Node",
            "node_detail": [
                {"code": "JKT", "name": "Jakarta"},
                {"code": "JKTBR", "name": "Jakarta Barat", "parent": "Jakarta"},
                {"code": "JKTSL", "name": "Jakarta Selatan", "parent": "Jakarta"},
                {"code": "JKTUT", "name": "Jakarta Utara", "parent": "Jakarta"},
                {"code": "JKTTR", "name": "Jakarta Timur", "parent": "Jakarta"},
                {"code": "JKTPT", "name": "Jakarta Pusat", "parent": "Jakarta"},
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

        # GET LIST OF NODE DETAIL
        data = self.client.get(f"/api/node-detail/{node_id}", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        for each in result:
            each.pop("id")
        jakarta_id = NodeDetail.objects.get(name="Jakarta").id
        expected_result = [
            {"code": "BLI", "name": "Bali", "parent_id": None},
            {"code": "DIY", "name": "Daerah Istimewa Yogyakarta", "parent_id": None},
            {"code": "JKT", "name": "Jakarta", "parent_id": None},
            {"code": "JKTBR", "name": "Jakarta Barat", "parent_id": jakarta_id},
            {"code": "JKTSL", "name": "Jakarta Selatan", "parent_id": jakarta_id},
            {"code": "JKTUT", "name": "Jakarta Utara", "parent_id": jakarta_id},
            {"code": "JKTTR", "name": "Jakarta Timur", "parent_id": jakarta_id},
            {"code": "JKTPT", "name": "Jakarta Pusat", "parent_id": jakarta_id},
        ]
        self.assertEqual(result, expected_result)

    def test_upload_csv_node(self):
        # POST DATA
        pd.DataFrame(
            [
                {"name": "Jawa Barat", "code": "JWB", "parent": None},
                {"name": "Banten", "code": "BTN", "parent": None},
                {"name": "Bandung", "code": "BDG", "parent": "Jawa Barat"},
            ]
        ).to_csv("./node.csv", index=False)
        data = self.client.post(
            "/api/node-upload",
            {
                "file": open("./node.csv", "rb"),
                "name": "New Node",
            },
            format="multipart",
        )
        self.assertEqual(data.status_code, 200)

        # GET LIST OF NODE DETAIL
        node_id = Node.objects.filter(name="New Node").first().id
        data = self.client.get(f"/api/node-detail/{node_id}", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        for each in result:
            each.pop("id")
        jawa_barat_id = NodeDetail.objects.get(name="Jawa Barat").id
        expected_result = [
            {"code": "JWB", "name": "Jawa Barat", "parent_id": None},
            {"code": "BTN", "name": "Banten", "parent_id": None},
            {"code": "BDG", "name": "Bandung", "parent_id": jawa_barat_id},
        ]
        self.assertEqual(result, expected_result)

        # Remove file
        os.remove("./node.csv")
