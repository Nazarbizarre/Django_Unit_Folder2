from django.urls import path, include

from .views import register

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
]