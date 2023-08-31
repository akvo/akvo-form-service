from django.urls import re_path

from akvo.core_data.views.data import DataView

urlpatterns = [
    re_path(r"data/(?P<form_id>[0-9]+)", DataView.as_view()),
]
