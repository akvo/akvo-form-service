from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from akvo.core_node.models import Node
from akvo.core_node.serializers.node import (
    AddNodeSerializer,
    ListNodeSerializer,
    UploadCSVNodeSerializer,
)
from akvo.utils.custom_serializer_fields import validate_serializers_message
from akvo.utils.default_serializers import DefaultResponseSerializer


class NodeView(APIView):
    @extend_schema(
        responses={200: ListNodeSerializer(many=True)},
        tags=["Node"],
        summary="Get Node",
    )
    def get(self, request):
        nodes = Node.objects.all()
        return Response(
            ListNodeSerializer(instance=nodes, many=True).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=AddNodeSerializer,
        responses={200: DefaultResponseSerializer},
        tags=["Node"],
        summary="Add Node",
    )
    def post(self, request):
        serializer = AddNodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": validate_serializers_message(serializer.errors),
                    "details": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


@extend_schema(
    request=UploadCSVNodeSerializer,
    responses={200: DefaultResponseSerializer},
    tags=["Node"],
    summary="Upload CSV Node",
)
@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_csv_node(request):
    serializer = UploadCSVNodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "message": validate_serializers_message(serializer.errors),
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer.save()
    return Response({"message": "ok"}, status=status.HTTP_200_OK)
