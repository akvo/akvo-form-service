from django.urls import re_path
from .views import upload_images

urlpatterns = [
    re_path(r"^upload/images", upload_images),
]
