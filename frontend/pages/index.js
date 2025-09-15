// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\pages\index.js

import { useState, useCallback } from 'react';
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import Chart from '@/components/Chart';
import LogsTable from '@/components/LogsTable';
import useWebSocket from '@/hooks/useWebSocket';

export default function Dashboard() {
  const [logs, setLogs] = useState([]);

  const handleLogMessage = useCallback((log) => {
    setLogs((prevLogs) => [log, ...prevLogs.slice(0, 99)]); // Limit to 100 logs
  }, []);

  useWebSocket('ws://localhost:8000/ws/logs', handleLogMessage);

  // 🔢 Process logs for error frequency (grouped by 10 logs each)
  const chartData = logs
    .slice(0, 50)
    .reduce((acc, log, idx) => {
      const severity = (log.severity || log.level || '').toUpperCase();
      const isError = ['ERROR', 'CRITICAL'].includes(severity);
      const groupIndex = Math.floor(idx / 10);

      if (!acc[groupIndex]) {
        acc[groupIndex] = { label: `#${groupIndex + 1}`, errors: 0 };
      }

      if (isError) acc[groupIndex].errors += 1;

      return acc;
    }, []);

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 p-6">
        <h2 className="text-2xl font-bold mb-6">🚨 Realtime Monitoring Dashboard</h2>

        {/* 📊 Error Frequency Chart */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-white shadow-md rounded-xl p-4">
            <h3 className="text-lg font-semibold mb-2">📊 Error Frequency</h3>
            {chartData.length > 0 ? (
              <Chart data={chartData} />
            ) : (
              <p className="text-gray-500">Waiting for logs to show chart.</p>
            )}
          </div>
        </div>

        {/* 📜 Real-time Logs Table */}
        <div className="bg-white shadow-md rounded-xl p-4">
          {/* <h3 className="text-lg font-semibold mb-2">📜 Real time Logs</h3> */}
          {logs.length > 0 ? (
            <LogsTable initialLogs={logs} />
          ) : (
            <p className="text-gray-500">Waiting for logs...</p>
          )}
        </div>
      </div>
    </div>
  );
}
