from django.urls import path

from akvo.core_node.views.node import NodeView

urlpatterns = [
    path("node", NodeView.as_view()),
]
