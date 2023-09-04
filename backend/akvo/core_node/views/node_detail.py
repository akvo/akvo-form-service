from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from akvo.core_node.models import Node, NodeDetail
from akvo.core_node.serializers.node_detail import ListNodeDetailSerializer


@extend_schema(
    responses={200: ListNodeDetailSerializer(many=True)},
    tags=["Node"],
    summary="To get list of node details by node id",
    description="Get list of node details by node id",
)
@api_view(["GET"])
def get_node_detail_by_node_id(request, node_id):
    node = get_object_or_404(Node, pk=node_id)
    instance = NodeDetail.objects.filter(node=node).all()
    return Response(
        ListNodeDetailSerializer(instance=instance, many=True).data,
        status=status.HTTP_200_OK,
    )
