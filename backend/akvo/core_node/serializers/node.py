from rest_framework import serializers

from akvo.core_node.models import Node, NodeDetail
from akvo.utils.custom_serializer_fields import (
    CustomCharField,
)
from akvo.core_node.serializers.node_detail import (
    AddNodeDetailSerializer
)


class AddNodeSerializer(serializers.Serializer):
    name = CustomCharField(allow_null=False)
    node_detail = AddNodeDetailSerializer(many=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_name(self, value):
        if not value or value == "":
            raise serializers.ValidationError("Node name is required")
        return value

    def create(self, validated_data):
        obj_node = Node.objects.create(
            name=validated_data.get("name")
        )
        for nd in validated_data.get("node_detail"):
            NodeDetail.objects.create(
                node=obj_node,
                code=nd.get('code'),
                name=nd.get('name')
            )
        return object
