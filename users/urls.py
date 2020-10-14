from django.urls import path

from .views import regiser

urlpatterns = [
    path('', regiser, name='register-user')
]