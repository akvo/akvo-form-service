from django.urls import path, re_path

from akvo.core_node.views.node import (
    NodeView, upload_csv_node,
)
from akvo.core_node.views.node_detail import get_node_detail_by_node_id

urlpatterns = [
    path("node", NodeView.as_view()),
    re_path(
        r"node-detail/(?P<node_id>[0-9]+)/(?P<parent_id>[0-9]+)",
        get_node_detail_by_node_id,
    ),
    re_path(r"node-upload", upload_csv_node),
]
