from drf_spectacular.utils import extend_schema

from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from akvo.core_node.models import Node, NodeDetail
from akvo.core_node.serializers.node_detail import ListNodeDetailSerializer


class NodeDetailQuerySerializer(serializers.Serializer):
    parent_id = serializers.IntegerField(default=0, required=False)


@extend_schema(
    responses={200: ListNodeDetailSerializer(many=True)},
    tags=["Node"],
    summary="To get list of node details by node id",
    description="Get list of node details by node id",
)
@api_view(["GET"])
def get_node_detail_by_node_id(request, node_id, parent_id):
    if parent_id == "0":
        parent_id = None
    node = get_object_or_404(Node, pk=node_id)
    instance = NodeDetail.objects.filter(node=node, parent=parent_id).all()
    return Response(
        ListNodeDetailSerializer(instance=instance, many=True).data,
        status=status.HTTP_200_OK,
    )
