from django.urls import path
from .views import *

urlpatterns = [
    path('request/', RequestOTP.as_view()),
    path('verify/', VerifyOTP.as_view()),
]