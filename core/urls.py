"""
URL configuration for helper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(
    public=True,
    permission_classes=[
        permissions.IsAuthenticated,
    ],
    authentication_classes=[
        BasicAuthentication,
    ],
)

urlpatterns = [
    path(
        "api/schema/",
        login_required(SpectacularAPIView.as_view(), login_url="/admin/login/"),
        name="schema",
    ),
    path(
        "docs",
        login_required(
            SpectacularSwaggerView.as_view(url_name="schema"), login_url="/admin/login/"
        ),
        name="swagger-ui",
    ),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls'))
]
