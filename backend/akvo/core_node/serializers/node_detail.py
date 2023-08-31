from rest_framework import serializers

from akvo.core_node.models import NodeDetail
from akvo.utils.custom_serializer_fields import (
    CustomCharField,
)


class AddNodeDetailSerializer(serializers.ModelSerializer):
    code = CustomCharField(allow_null=False)
    name = CustomCharField(allow_null=False)

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
        fields = ["code", "name"]