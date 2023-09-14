from django.urls import re_path
from akvo.core_mobile.views.mobile_form import (
    get_mobile_form_definition,
    sync_form_data,
)

urlpatterns = [
    re_path(r"^device/forms/(?P<form_id>[0-9]+)", get_mobile_form_definition),
    re_path(r"^device/sync", sync_form_data),
]
