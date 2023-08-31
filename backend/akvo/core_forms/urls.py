from django.urls import path

from akvo.core_forms.views.form import list_form

urlpatterns = [
    path('forms', list_form),
]
