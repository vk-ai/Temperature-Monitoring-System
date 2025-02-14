import React from 'react';
import './App.css';
import TemperatureChart from './components/TemperatureChart';

function App() {
  return (
    <div className="App">
      <h1>Temperature Monitoring Dashboard</h1>
      <TemperatureChart />
    </div>
  );
}

export default App;
