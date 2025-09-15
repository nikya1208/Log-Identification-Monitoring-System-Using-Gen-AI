// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\pages\dashboard.js

import { useState, useCallback } from 'react';
import ErrorFrequencyChart from '@/components/ErrorFrequencyChart';
import AlertsFeed from '@/components/AlertsFeed';
import useWebSocket from '@/hooks/useWebSocket';

export default function Dashboard() {
  const [errorFrequencyData, setErrorFrequencyData] = useState([]);

  // 🧠 Handle incoming WebSocket messages
  const handleAlertMessage = useCallback((msg) => {
    const severity = (msg.severity || '').toUpperCase();
    const isError = ['HIGH', 'CRITICAL', 'ERROR'].includes(severity);

    if (isError) {
      setErrorFrequencyData((prev) => [
        ...prev.slice(-5),
        {
          time: new Date().toLocaleTimeString(),
          count: 1, // You can increase count if batching
        },
      ]);
    }
  }, []);

  // 🌐 Connect to WebSocket server
  useWebSocket('ws://localhost:8000/ws/alerts', handleAlertMessage);

  return (
    <div className="p-6 space-y-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold">📈 Realtime Monitoring Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <ErrorFrequencyChart data={errorFrequencyData} />
        </div>
        <div>
          <AlertsFeed />
        </div>
      </div>
    </div>
  );
}
