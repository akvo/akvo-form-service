"""afs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("api/", include("akvo.core_forms.urls"), name="core_forms"),
    path("api/", include("akvo.core_data.urls"), name="core_data"),
    path("api/", include("akvo.core_node.urls"), name="core_node"),
    path("api/", include("akvo.core_storage.urls"), name="core_storage"),
    path("api/", include("akvo.core_mobile.urls"), name="core_mobile"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
]
