from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

management_urls = [
    path("admin/", admin.site.urls),
    path("schema/download/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

app_urls = [
    path("users/", include("app.users.urls", namespace="users")),
]

urlpatterns = [*management_urls, *app_urls]
