from django.urls import path
from .pushingpay_webhook import pushinpay_webhook_handler

urlpatterns = [
    path('', pushinpay_webhook_handler, name='pushinpay_webhook'),
]