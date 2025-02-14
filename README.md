# MBK Backend - Temperature Monitoring System

A Django-based backend system for monitoring and predicting CPU and battery temperatures.
## Machine Learning Model

The system uses a Long Short-Term Memory (LSTM) neural network for temperature prediction. The LSTM model:
- Takes historical temperature data as input
- Predicts both CPU and battery temperatures for future time intervals
- Is trained on sequences of past temperature readings
- Can capture long-term dependencies in the temperature patterns
- Updates predictions in real-time as new data arrives


## Technology Stack

- **Django**: Web framework for building the backend
- **Django REST Framework**: For creating RESTful APIs
- **SQLite**: Default database for storing temperature records
- **Python**: Programming language (3.8+)
- **TensorFlow**: For building and training the LSTM model
- **Scikit-learn**: For linear regression models

## Project Structure

The project consists of a `monitor` app that handles:
- Temperature data collection and storage
- Temperature prediction functionality
- RESTful API endpoints for data access

### Key Components

- `models.py`: Defines Temperature and PredictedTemperature models
- `serializers.py`: REST framework serializers for data transformation
- `tests.py`: Comprehensive test suite for API endpoints
- `admin.py`: Django admin interface configuration

## Setup Instructions

1. Clone the repository:
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the development server:

```bash
python manage.py runserver
```

4. Access the admin interface:

    http://127.0.0.1:8000/admin/

5. Run tests:

```bash
python manage.py test
``` 