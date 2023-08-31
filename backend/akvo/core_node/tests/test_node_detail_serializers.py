from django.test import TestCase
from rest_framework.test import APIClient

from akvo.core_node.models import Node, NodeDetail
from akvo.core_node.serializers.node_detail import (
    ListNodeDetailSerializer
)


class TestNodeDetailSerializers(TestCase):
    def setUp(self):
        self.client = APIClient()
        node_data = {
            "name": "Indonesia Province"
        }
        self.node = Node.objects.create(**node_data)
        self.data = {
            "node": self.node,
            "code": "DPS",
            "name": "Denpasar"
        }
        self.instance = NodeDetail.objects.create(**self.data)
        self.serializer = ListNodeDetailSerializer(instance=self.instance)

    def test_list_node_detail_serializer_return_expected_data(self):
        data = self.serializer.data
        expected_data = {
            "id": data.get("id"),
            "code": "DPS",
            "name": "Denpasar"
        }
        self.assertEqual(data, expected_data)
