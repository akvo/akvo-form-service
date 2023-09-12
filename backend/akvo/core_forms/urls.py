from django.urls import path, re_path

from akvo.core_forms.views.form import (
    list_form, get_form_by_id,
    FormManagementView
)

urlpatterns = [
    path('forms', list_form),
    re_path(r"^form/(?P<form_id>[0-9]+)", get_form_by_id),
    path('form', FormManagementView.as_view()),
]
