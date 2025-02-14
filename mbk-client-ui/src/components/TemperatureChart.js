import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";
// API endpoints
const TEMPERATURE_API_URL = "http://127.0.0.1:8000/api/temperatures/";
const TEMPERATURE_PREDICTION_API_URL = "http://127.0.0.1:8000/api/temperature/predict/";

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

const TemperatureChart = () => {
  const [data, setData] = useState([]);
  const [predictedData, setPredictedData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch temperature data from the API
  const fetchTemperatureData = async () => {
    try {
      const response = await axios.get(TEMPERATURE_API_URL);
      setData(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching temperature data:", error);
      setLoading(false);
    }
  };
  
  // Fetch prediction data from the API
  const fetchPredictionData = async () => {
    try {
      const response = await axios.get(TEMPERATURE_PREDICTION_API_URL);
      setPredictedData((prevData) => [...prevData, ...response.data]); // Append predictions to the existing data
    } catch (error) {
      console.error("Error fetching prediction data:", error);
    }
  };

  // Fetch data initially and then every 5 seconds
  useEffect(() => {
    fetchTemperatureData();
    fetchPredictionData();

    const intervalId = setInterval(() => {
      fetchTemperatureData();
      fetchPredictionData();
    }, 5000);

    return () => clearInterval(intervalId);
  }, []);

  // Prepare data for Chart.js (Historical Data)
  const chartData = {
    labels: data.map((entry) => new Date(entry.timestamp).toLocaleTimeString()), // Time of measurement
    datasets: [
      {
        label: "CPU Temperature (°C)",
        data: data.map((entry) => entry.cpu_temp),
        borderColor: "rgba(255, 99, 132, 1)",
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        fill: true,
      },
      {
        label: "Battery Temperature (°C)",
        data: data.map((entry) => entry.battery_temp),
        borderColor: "rgba(54, 162, 235, 1)",
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        fill: true,
      },
    ],
  };

  // Prepare data for Prediction Chart (Predicted Data)
  const predictionChartData = {
    labels: [
      ...data.map((entry) => new Date(entry.timestamp).toLocaleTimeString()),
      ...predictedData.map((entry) => new Date(entry.timestamp).toLocaleTimeString()),
    ],
    datasets: [
      {
        label: "Predicted CPU Temperature (°C)",
        data: [
          ...data.map(() => null), // Placeholder for historical data
          ...predictedData.map((entry) => entry.predicted_cpu_temp),
        ],
        borderColor: "rgba(255, 159, 64, 1)",
        backgroundColor: "rgba(255, 159, 64, 0.2)",
        fill: true,
        borderDash: [5, 5], // Dashed line for prediction
      },
      {
        label: "Predicted Battery Temperature (°C)",
        data: [
          ...data.map(() => null), // Placeholder for historical data
          ...predictedData.map((entry) => entry.predicted_battery_temp),
        ],
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        fill: true,
        borderDash: [5, 5], // Dashed line for prediction
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: "top" },
    },
  };

  return (
    <div>
      <h2>MacBook Temperature Monitoring</h2>
      
      {/* Historical Data Chart */}
      {loading ? (
        <p>Loading data...</p>
      ) : (
        <div style={{ position: "relative", height: "400px" }}>
          <Line data={chartData} options={chartOptions} />
        </div>
      )}

      {/* Prediction Data Chart */}
      {loading ? (
        <p>Loading prediction data...</p>
      ) : (
        <div style={{ position: "relative", height: "400px", marginTop: "50px" }}>
          <h3>Predicted Temperatures</h3>
          <Line data={predictionChartData} options={chartOptions} />
        </div>
      )}
    </div>
    
  );
};

export default TemperatureChart;
