from rest_framework import serializers

import pandas as pd
from django.core.validators import FileExtensionValidator
from akvo.core_node.models import Node, NodeDetail
from akvo.utils.custom_serializer_fields import (
    CustomCharField,
)
from akvo.core_node.serializers.node_detail import AddNodeDetailSerializer


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
        node = Node.objects.get_or_create(name=validated_data.get("name"))
        obj_node = node[0]
        for nd in validated_data.get("node_detail"):
            parent = None
            if nd.get("parent"):
                parent = NodeDetail.objects.filter(name=nd.get("parent")).first()
            NodeDetail.objects.create(
                node=obj_node, parent=parent, code=nd.get("code"), name=nd.get("name")
            )
        return object


class UploadCSVNodeSerializer(serializers.Serializer):
    file = serializers.FileField(
        allow_null=False,
        validators=[FileExtensionValidator(["csv"])],
    )
    name = serializers.CharField(allow_null=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_name(self, value):
        if not value or value == "":
            raise serializers.ValidationError("Node name is required")
        return value

    def validate_csv_file(self, value):
        df = pd.read_csv(value)
        if "parent" not in df.columns:
            raise serializers.ValidationError("Column parent is required")
        if "name" not in df.columns:
            raise serializers.ValidationError("Column name is required")
        return value

    def create(self, validated_data):
        node_name = validated_data.get("name")
        node = Node.objects.create(name=node_name)
        csv_file = validated_data.get("file")
        df = pd.read_csv(csv_file)
        df = df.where(pd.notnull(df), None)
        for index, row in df.iterrows():
            parent = None
            if row["parent"]:
                parent = NodeDetail.objects.filter(name=row["parent"]).first()
            NodeDetail.objects.create(
                node=node, parent=parent, code=row["code"], name=row["name"]
            )
        return object
