from django.urls import path, include
from backend.views import telegram

urlpatterns = [
    path('', telegram),
]
