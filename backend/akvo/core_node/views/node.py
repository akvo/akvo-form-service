import os
import mimetypes

from django.http import HttpResponse
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
from afs.settings import BASE_DIR


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


@extend_schema(tags=["Node"], summary="Get SQLITE File")
@api_view(["GET"])
def download_sqlite_file(request, file_name):
    file_path = os.path.join(BASE_DIR, f"./source/sqlite/{file_name}")
    print(file_path, file_name, '=========')
    # Check if file exists and is accessible
    if not os.path.exists(file_path):
        return HttpResponse(
            {"message": "File not found."}, status=status.HTTP_404_NOT_FOUND
        )
    # Get the file's content type
    content_type, _ = mimetypes.guess_type(file_path)
    # Read the file content into a variable
    with open(file_path, "rb") as file:
        file_content = file.read()
    # Create the response and set the appropriate headers
    response = HttpResponse(file_content, content_type=content_type)
    response["Content-Length"] = os.path.getsize(file_path)
    response["Content-Disposition"] = "attachment; filename=%s" % file_name
    return response
