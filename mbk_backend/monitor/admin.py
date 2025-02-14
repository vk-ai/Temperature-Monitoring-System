from django.contrib import admin
from .models import Temperature, PredictedTemperature
# Register your models here.



admin.site.register(Temperature)
admin.site.register(PredictedTemperature)
