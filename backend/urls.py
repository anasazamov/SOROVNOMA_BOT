from django.urls import path, include
from backend.views import AdminBot

urlpatterns = [
    path('<str:token>', AdminBot.as_view()),
]
