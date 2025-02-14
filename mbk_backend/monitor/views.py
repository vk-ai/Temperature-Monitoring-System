import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Temperature, PredictedTemperature
from .serializers import TemperatureSerializer, PredictedTemperatureSerializer
from datetime import datetime, timedelta


"""
Handles POST requests for temperature data.

This method validates and saves temperature readings submitted via POST requests.
It uses the TemperatureSerializer to validate the incoming data and create new
Temperature model instances in the database.

Args:
    request: The HTTP request object containing temperature data in the request body.
            Expected format:
            {
                "cpu_temp": float,
                "battery_temp": float,
                "timestamp": datetime string
            }

Returns:
    Response: A REST framework Response object containing:
        - On success (HTTP 201):
            - The serialized temperature data that was saved
        - On validation failure (HTTP 400):
            - Error details explaining why the validation failed

Example:
    POST /api/temperature/
    {
        "cpu_temp": 45.2,
        "battery_temp": 39.8,
        "timestamp": "2024-03-15T14:30:00Z"
    }
"""
class TemperatureAPI(APIView):
    def get(self, request):
        temps = Temperature.objects.all().order_by('-timestamp')[:10]
        serializer = TemperatureSerializer(temps, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TemperatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
"""
Handles GET requests for temperature predictions.

This view uses historical temperature data to predict future CPU and battery temperatures
using linear regression models. It performs the following steps:

1. Retrieves all historical temperature records from the database, ordered by timestamp
2. Converts the data into a pandas DataFrame for analysis
3. Processes timestamps into Unix timestamp format for numerical analysis
4. Trains two separate LinearRegression models:
   - One for CPU temperature predictions
   - One for battery temperature predictions
5. Makes predictions for temperatures 1 hour into the future
6. Saves the predictions to the database using the PredictedTemperature model
7. Returns the 10 most recent temperature predictions

Args:
    request: The HTTP GET request object

Returns:
    Response: A REST framework Response object containing:
        - The 10 most recent temperature predictions, serialized as JSON
        - Each prediction includes:
            - timestamp: The future timestamp for the prediction
            - predicted_cpu_temp: Predicted CPU temperature
            - predicted_battery_temp: Predicted battery temperature

Example response:
    [
        {
            "timestamp": "2024-03-15T15:30:00Z",
            "predicted_cpu_temp": 46.8,
            "predicted_battery_temp": 40.2
        },
        ...
    ]

Technical Details:
    - Uses scikit-learn's LinearRegression for prediction
    - Converts timestamps to Unix format for numerical processing
    - Predicts temperatures 1 hour (3600 seconds) into the future
    - Stores predictions in PredictedTemperature model
"""

class TemperaturePredictionView(APIView):
    def get(self, request):
        # Fetch historical data from the database (CPU and GPU temperatures)
        temperatures = Temperature.objects.all().order_by('timestamp')
        
        # Prepare the data for the model
        data = pd.DataFrame(list(temperatures.values('timestamp', 'cpu_temp', 'battery_temp')))
        
        # Feature extraction (timestamps to numerical values for prediction)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['timestamp'] = data['timestamp'].apply(lambda x: x.timestamp())  # Convert to Unix timestamp
        
        # Prepare features and target variables
        X = data['timestamp'].values.reshape(-1, 1)  # Features: Timestamps
        y_cpu = data['cpu_temp'].values  # Target: CPU Temperature
        y_battery = data['battery_temp'].values  # Target: GPU Temperature
        
        # Train a linear regression model for CPU and GPU temperatures
        model_cpu = LinearRegression().fit(X, y_cpu)
        model_battery = LinearRegression().fit(X, y_battery)
        
        # Make predictions for the next timestamp (for example, predict for 1 hour ahead)
        future_timestamp = np.array([[data['timestamp'].max() + 3600]])  # 1 hour ahead (3600 seconds)
        predicted_cpu_temp = model_cpu.predict(future_timestamp)[0]
        predicted_battery_temp = model_battery.predict(future_timestamp)[0]
        
        # Convert the future timestamp back to a datetime object
        future_datetime = datetime.utcfromtimestamp(future_timestamp[0][0])
        
        # Create a new record in the database with the predicted temperatures
        new_temp = PredictedTemperature(
            timestamp=future_datetime,
            predicted_cpu_temp=predicted_cpu_temp,
            predicted_battery_temp=predicted_battery_temp
        )
        new_temp.save()

        temps = PredictedTemperature.objects.all().order_by('-timestamp')[:10]
        serializer = PredictedTemperatureSerializer(temps, many=True)
        return Response(serializer.data)