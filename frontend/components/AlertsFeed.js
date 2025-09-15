// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\components\AlertsFeed.js

import React, { useEffect, useState } from 'react';
import useWebSocket from '../hooks/useWebSocket'; // Import the new hook

export default function AlertsFeed() {
  const [alerts, setAlerts] = useState([]); // Manage alerts state
  const [error, setError] = useState(null);
  const { connectionStatus } = useWebSocket(
    "ws://localhost:8000/ws/alerts", // WebSocket URL for alerts
    (message) => {
      if (message.type === "alert") {
        setAlerts((prevAlerts) => [message, ...prevAlerts]); // Prepend new alerts to the list
      }
    },
    {
      onError: (error) => setError(`WebSocket Error: ${error.message}`),
    }
  );

  useEffect(() => {
    if (connectionStatus === 'disconnected') {
      setError("WebSocket connection lost. Reconnecting...");
    }
  }, [connectionStatus]);

  return (
    <div className="p-4 bg-white rounded-2xl shadow-md">
      <h2 className="text-xl font-semibold mb-4">🚨 Live Alerts</h2>

      {error && (
        <div className="text-red-600 mb-3">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="max-h-[400px] overflow-y-auto space-y-3">
        {alerts.length === 0 && (
          <p className="text-gray-500">No alerts yet. Waiting for updates...</p>
        )}
        {alerts.map((alert, index) => (
          <div
            key={index}
            className={`p-3 rounded-xl border ${
              alert.severity === 'HIGH'
                ? 'border-red-400 bg-red-100'
                : alert.severity === 'WARNING'
                ? 'border-yellow-400 bg-yellow-100'
                : 'border-gray-300 bg-gray-100'
            }`}
          >
            <p className="font-medium">{alert.title || alert.message}</p>
            <p className="text-sm text-gray-600">
              {new Date(alert.timestamp).toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
