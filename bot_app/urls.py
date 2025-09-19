from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('setup-admin/', views.setup_admin, name='setup_admin'),
]