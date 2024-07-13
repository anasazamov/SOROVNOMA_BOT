from django.urls import path, include
from backend.views import AdminBot

urlpatterns = [
    path('', AdminBot.as_view()),
]
