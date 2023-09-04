from rest_framework import serializers
from collections import OrderedDict

from akvo.core_node.models import NodeDetail
from akvo.utils.custom_serializer_fields import (
    CustomCharField,
)


class AddNodeDetailSerializer(serializers.ModelSerializer):
    code = CustomCharField(allow_null=False)
    name = CustomCharField(allow_null=False)
    parent = CustomCharField(allow_null=True, required=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_code(self, value):
        if not value or value == "":
            raise serializers.ValidationError("Node detail code is required")
        return value

    def validate_name(self, value):
        if not value or value == "":
            raise serializers.ValidationError("Node detail name is required")
        return value

    class Meta:
        model = NodeDetail
        fields = ["parent", "code", "name"]


class ListNodeDetailSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(
        source="parent.id", read_only=True, allow_null=True
    )

    class Meta:
        model = NodeDetail
        fields = ["id", "parent_id", "code", "name"]
