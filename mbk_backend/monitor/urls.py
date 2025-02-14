from django.urls import path
from .views import TemperatureAPI, TemperaturePredictionView

urlpatterns = [
    path('api/temperatures/', TemperatureAPI.as_view(), name='temperature_api'),
    path('api/temperature/predict/', TemperaturePredictionView.as_view(), name='temperature-predict'),
]