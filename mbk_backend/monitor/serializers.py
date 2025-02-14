from rest_framework import serializers
from .models import Temperature, PredictedTemperature

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ['timestamp', 'cpu_temp', 'battery_temp']


class PredictedTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictedTemperature
        fields = ['timestamp', 'predicted_cpu_temp', 'predicted_battery_temp']