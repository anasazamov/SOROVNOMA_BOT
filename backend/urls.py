from django.urls import path, include
from backend.views import AdminBotView

urlpatterns = [
    path('', AdminBotView.as_view()),
]
