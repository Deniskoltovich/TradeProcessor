from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.urls", "accounts")),
    path("assets/", include('assets.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('orders/', include('orders.urls')),
]
