from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('health-check', views.HealthCheck.as_view(), name='health-check')
]