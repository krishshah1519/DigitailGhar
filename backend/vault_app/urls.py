from django.urls import path
from .views import *

urlpatterns =[
    path('register/', RegisterAPIView.as_view()),
    path('verify/', VerifyOTPAPIView.as_view()),
]