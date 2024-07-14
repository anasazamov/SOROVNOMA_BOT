from django.urls import path
from backend.views import telegram,telegram2

urlpatterns = [
    path('', telegram),
    path('<str:token>', telegram2),
]
