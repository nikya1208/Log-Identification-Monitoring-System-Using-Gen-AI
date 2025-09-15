// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\components\LogDashboard.js

import { useState, useCallback } from "react";
import useWebSocket from "@/hooks/useWebSocket";

export default function LogDashboard() {
  const [logs, setLogs] = useState([]);

  const handleLogMessage = useCallback((log) => {
    setLogs((prev) => [log, ...prev.slice(0, 99)]); // Limit to last 100 logs
  }, []);

  useWebSocket("ws://localhost:8000/ws/logs", handleLogMessage);

  return (
    <div className="p-4 max-h-[80vh] overflow-y-auto bg-zinc-900 text-white rounded-lg shadow-lg space-y-2">
      <h2 className="text-2xl font-semibold mb-4">📡 Live Logs</h2>
      {logs.length === 0 ? (
        <p className="text-gray-400">Waiting for logs...</p>
      ) : (
        logs.map((log, index) => (
          <div
            key={index}
            className={`p-3 rounded-md shadow-sm ${
              log.level === "ERROR"
                ? "bg-red-600"
                : log.level === "WARNING"
                ? "bg-yellow-600 text-black"
                : "bg-green-700"
            }`}
          >
            <div className="text-sm opacity-75">{log.timestamp}</div>
            <div className="font-mono">{log.message}</div>
          </div>
        ))
      )}
    </div>
  );
}
