from django.test import TestCase
from rest_framework import serializers

from akvo.core_node.serializers.node import (
    AddNodeSerializer
)
from akvo.core_node.serializers.node_detail import (
    AddNodeDetailSerializer
)


class TestNodeSerializers(TestCase):
    def test_add_node_detail_serializer(self):
        # invalid value without name
        invalid_post_data = {
            'name': None,
            'code': 'ND01'
        }
        serializer = AddNodeDetailSerializer(data=invalid_post_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        # invalid value without code
        invalid_post_data = {
            'name': 'Node detail 1',
            'code': None
        }
        serializer = AddNodeDetailSerializer(data=invalid_post_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        # correct value
        post_data = {
            'name': 'Node detail 1',
            'code': 'ND01'
        }
        serializer = AddNodeDetailSerializer(data=post_data)
        self.assertTrue(serializer.is_valid())

    def test_add_node_serializer(self):
        post_node_details = {
            'name': 'Node detail 1',
            'code': 'ND01'
        }
        # invalid post node without name
        invalid_post_node = {
            'name': None,
            'node_detail': [post_node_details]
        }
        serializer = AddNodeSerializer(data=invalid_post_node)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        # correct post value
        post_node = {
            'name': 'Example Node 1',
            'node_detail': [post_node_details]
        }
        serializer = AddNodeSerializer(data=post_node)
        self.assertTrue(serializer.is_valid())
