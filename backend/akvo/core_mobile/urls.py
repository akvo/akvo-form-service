from django.urls import re_path
from akvo.core_mobile.views.mobile_form import (
    get_mobile_form_definition,
)

urlpatterns = [
    re_path(
        r"form/(?P<form_id>[0-9]+)", get_mobile_form_definition
    ),
]
