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

        # GET LIST OF NODE
        data = self.client.get("/api/node", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        expected_result = [
            {
                "id": node_id,
                "name": "Example Node",
                "endpoint": f"/api/node/{node_id}",
                "initial": 0,
            },
        ]
        self.assertEqual(result, expected_result)

        # GET LIST OF NODE DETAIL
        data = self.client.get(f"/api/node-detail/{node_id}/0", follow=True)
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
        data = self.client.get(f"/api/node-detail/{node_id}/0", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        for each in result:
            each.pop("id")
        expected_result = [
            {"code": "BLI", "name": "Bali", "parent_id": None},
            {"code": "DIY", "name": "Daerah Istimewa Yogyakarta", "parent_id": None},
            {"code": "JKT", "name": "Jakarta", "parent_id": None},
        ]
        self.assertEqual(result, expected_result)

    def test_upload_csv_node_with_children(self):
        pd.DataFrame(
            [
                {"name": "Jawa Barat", "code": "JWB", "parent": None},
                {"name": "Banten", "code": "BTN", "parent": None},
                {"name": "Bogor", "code": "BGR", "parent": "Jawa Barat"},
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
        data = self.client.get(f"/api/node-detail/{node_id}/0", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        for each in result:
            each.pop("id")
        expected_result = [
            {"code": "JWB", "name": "Jawa Barat", "parent_id": None},
            {"code": "BTN", "name": "Banten", "parent_id": None},
        ]
        self.assertEqual(result, expected_result)

        # GET LIST OF NODE DETAIL CHILDREN
        jawa_barat_id = NodeDetail.objects.get(name="Jawa Barat").id
        data = self.client.get(
            f"/api/node-detail/{node_id}/{jawa_barat_id}", follow=True
        )
        self.assertEqual(data.status_code, 200)
        result = data.json()
        for each in result:
            each.pop("id")
        expected_result = [
            {"code": "BGR", "name": "Bogor", "parent_id": jawa_barat_id},
        ]
        self.assertEqual(result, expected_result)

        # WRONG ENDPOINT
        data = self.client.get(f"/api/node-detail/{node_id}", follow=True)
        self.assertEqual(data.status_code, 404)

        # WRONG PARENT ID
        data = self.client.get(f"/api/node-detail/{node_id}/999", follow=True)
        self.assertEqual(data.json(), [])

        # Remove file
        os.remove("./node.csv")

    def test_upload_csv_node_without_children(self):
        node = pd.DataFrame(
            [
                {"name": "Jawa Barat", "code": "JWB", "parent": None},
                {"name": "Banten", "code": "BTN", "parent": None},
            ]
        )
        node.to_csv("./node.csv", index=False)
        data = self.client.post(
            "/api/node-upload",
            {
                "file": open("./node.csv", "rb"),
                "name": "New Node Without Children",
            },
            format="multipart",
        )
        self.assertEqual(data.status_code, 200)

        # GET LIST OF NODE DETAIL
        node_id = Node.objects.filter(name="New Node Without Children").first().id
        data = self.client.get(f"/api/node-detail/{node_id}/0", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        for each in result:
            each.pop("id")
        expected_result = [
            {"code": "JWB", "name": "Jawa Barat", "parent_id": None},
            {"code": "BTN", "name": "Banten", "parent_id": None},
        ]
        self.assertEqual(result, expected_result)

        # Remove file
        os.remove("./node.csv")

    def test_upload_csv_node_without_code(self):

        pd.DataFrame(
            [
                {"name": "Jawa Barat", "parent": None},
                {"name": "Banten", "parent": None},
                {"name": "Bandung", "parent": "Jawa Barat"},
            ]
        ).to_csv("./node.csv", index=False)
        data = self.client.post(
            "/api/node-upload",
            {
                "file": open("./node.csv", "rb"),
                "name": "New Node without code",
            },
            format="multipart",
        )
        self.assertEqual(data.status_code, 200)

        # GET LIST OF NODE DETAIL
        node_id = Node.objects.filter(name="New Node without code").first().id
        data = self.client.get(f"/api/node-detail/{node_id}/0", follow=True)
        self.assertEqual(data.status_code, 200)
        result = data.json()
        for each in result:
            each.pop("id")
        expected_result = [
            {"code": None, "name": "Jawa Barat", "parent_id": None},
            {"code": None, "name": "Banten", "parent_id": None},
        ]
        self.assertEqual(result, expected_result)

        # Remove file
        os.remove("./node.csv")

    def test_upload_csv_node_with_wrong_parent(self):

        pd.DataFrame(
            [
                {"name": "Jawa Barat", "parent": None},
                {"name": "Banten", "parent": None},
                {"name": "Bandung", "parent": "Las Vegas"},
            ]
        ).to_csv("./node.csv", index=False)
        data = self.client.post(
            "/api/node-upload",
            {
                "file": open("./node.csv", "rb"),
                "name": "New Node with wrong parent",
            },
            format="multipart",
        )
        self.assertEqual(data.json(), {"message": "Parent not found"})
        self.assertEqual(data.status_code, 400)

        # Node is not created
        self.assertEqual(
            Node.objects.filter(name="New Node with wrong parent").count(), 0
        )

        # Remove file
        os.remove("./node.csv")

    def test_upload_csv_node_with_wrong_format(self):

        pd.DataFrame(
            [
                {"nm": "Jawa Barat", "parent": None},
                {"nm": "Banten", "parent": None},
                {"nm": "Bandung", "parent": "Las Vegas"},
            ]
        ).to_csv("./node.csv", index=False)
        data = self.client.post(
            "/api/node-upload",
            {
                "file": open("./node.csv", "rb"),
                "name": "New Node with wrong format",
            },
            format="multipart",
        )
        self.assertEqual(data.json(), {"message": "Name column is required"})
        self.assertEqual(data.status_code, 400)

        # Node is not created
        self.assertEqual(
            Node.objects.filter(name="New Node with wrong format").count(), 0
        )

        # Remove file
        os.remove("./node.csv")
