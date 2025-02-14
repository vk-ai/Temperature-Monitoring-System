from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from datetime import datetime, timedelta
import json

from .models import Temperature, PredictedTemperature
from .serializers import TemperatureSerializer, PredictedTemperatureSerializer

class TemperatureAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.temperature_url = reverse('temperature_api')
        
        # Create some test temperature data
        self.valid_temperature = {
            'cpu_temp': 45.2,
            'battery_temp': 39.8,
            'timestamp': datetime.now().isoformat()
        }
        
        self.invalid_temperature = {
            'cpu_temp': 'not a number',
            'battery_temp': 39.8,
            'timestamp': datetime.now().isoformat()
        }

        # Create some test records
        Temperature.objects.create(
            cpu_temp=42.0,
            battery_temp=38.0,
            timestamp=datetime.now() - timedelta(minutes=5)
        )
        Temperature.objects.create(
            cpu_temp=43.0,
            battery_temp=39.0,
            timestamp=datetime.now()
        )

    def test_create_valid_temperature(self):
        response = self.client.post(
            self.temperature_url,
            data=json.dumps(self.valid_temperature),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_temperature(self):
        response = self.client.post(
            self.temperature_url,
            data=json.dumps(self.invalid_temperature),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_temperatures(self):
        response = self.client.get(self.temperature_url)
        temperatures = Temperature.objects.all().order_by('-timestamp')[:10]
        serializer = TemperatureSerializer(temperatures, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TemperaturePredictionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prediction_url = reverse('temperature-predict')
        
        # Create historical temperature data for prediction
        timestamps = [
            datetime.now() - timedelta(minutes=15),
            datetime.now() - timedelta(minutes=10),
            datetime.now() - timedelta(minutes=5),
            datetime.now()
        ]
        
        for i, timestamp in enumerate(timestamps):
            Temperature.objects.create(
                cpu_temp=40.0 + i,
                battery_temp=35.0 + i,
                timestamp=timestamp
            )

    def test_get_temperature_predictions(self):
        response = self.client.get(self.prediction_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if predictions were made and saved
        self.assertTrue(PredictedTemperature.objects.exists())
        
        # Verify response structure
        self.assertTrue(isinstance(response.data, list))
        if len(response.data) > 0:
            prediction = response.data[0]
            self.assertIn('timestamp', prediction)
            self.assertIn('predicted_cpu_temp', prediction)
            self.assertIn('predicted_battery_temp', prediction)
            
            # Verify prediction values are reasonable
            self.assertTrue(isinstance(prediction['predicted_cpu_temp'], float))
            self.assertTrue(isinstance(prediction['predicted_battery_temp'], float))
            self.assertTrue(30 <= prediction['predicted_cpu_temp'] <= 100)  # reasonable temperature range
            self.assertTrue(30 <= prediction['predicted_battery_temp'] <= 100)  # reasonable temperature range
