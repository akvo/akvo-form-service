from django.urls import re_path

from akvo.core_data.views.data import DataView
from akvo.core_data.views.answer import AnswerView

urlpatterns = [
    re_path(r"data/(?P<form_id>[0-9]+)", DataView.as_view()),
    re_path(r"answers/(?P<data_id>[0-9]+)", AnswerView.as_view()),
]
