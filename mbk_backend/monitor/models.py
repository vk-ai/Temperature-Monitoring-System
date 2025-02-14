from django.db import models

# Create your models here.
class Temperature(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_temp = models.FloatField()
    battery_temp = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - CPU: {self.cpu_temp}°C, GPU: {self.battery_temp}°C"
    
    
class PredictedTemperature(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    predicted_cpu_temp = models.FloatField()
    predicted_battery_temp = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - CPU: {self.predicted_cpu_temp}°C, GPU: {self.predicted_battery_temp}°C"