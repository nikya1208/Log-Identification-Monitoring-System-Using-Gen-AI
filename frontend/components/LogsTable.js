// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\components\LogsTable.js

import { useEffect, useState, useCallback } from 'react';
import useWebSocket from '@/hooks/useWebSocket';

/**
 * LogsTable Component
 * @param {Array} initialLogs - Optional initial logs to pre-populate
 */
export default function LogsTable({ initialLogs = [] }) {
  const [logs, setLogs] = useState(initialLogs);
  const [severityFilter, setSeverityFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  // 🧠 Handle incoming WebSocket log
  const handleLogMessage = useCallback((log) => {
    setLogs((prev) => [log, ...prev.slice(0, 99)]);
  }, []);

  // 🌐 Start WebSocket connection
  useWebSocket('ws://localhost:8000/ws/logs', handleLogMessage);

  const filteredLogs = logs.filter((log) => {
    const level = (log.level || log.severity || '').toUpperCase();
    const message = (log.message || '').toLowerCase();

    const severityMatch = severityFilter === 'ALL' || level === severityFilter;
    const searchMatch = searchQuery === '' || message.includes(searchQuery.toLowerCase());

    return severityMatch && searchMatch;
  });

  return (
    <div className="space-y-3">
      {/* 🔍 Controls */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <h3 className="text-lg font-semibold">📜 Real time Logs</h3>
        <div className="flex gap-3 items-center">
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="px-3 py-1 border rounded-md shadow-sm text-sm"
          >
            <option value="ALL">All Severities</option>
            <option value="INFO">Info</option>
            <option value="WARNING">Warning</option>
            <option value="ERROR">Error</option>
            <option value="CRITICAL">Critical</option>
          </select>
          <input
            type="text"
            placeholder="🔍 Search logs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="px-3 py-1 border rounded-md shadow-sm text-sm w-60"
          />
        </div>
      </div>

      {/* 📋 Logs Table */}
      <div className="overflow-auto max-h-[400px] border rounded-xl shadow">
        {filteredLogs.length > 0 ? (
          <table className="w-full text-sm text-left text-gray-800">
            <thead className="bg-gray-100 sticky top-0 z-10">
              <tr>
                <th className="px-4 py-2">Time</th>
                <th className="px-4 py-2">Log Message</th>
                <th className="px-4 py-2">Severity</th>
                <th className="px-4 py-2">Source</th>
              </tr>
            </thead>
            <tbody>
              {filteredLogs.map((log, index) => (
                <tr
                  key={index}
                  className={`border-b hover:bg-gray-50 ${
                    index < 5 ? 'bg-yellow-50 animate-pulse' : ''
                  }`}
                >
                  <td className="px-4 py-2">{formatTime(log.time || log.timestamp)}</td>
                  <td className="px-4 py-2">{log.message}</td>
                  <td className={`px-4 py-2 font-semibold ${getSeverityClass(log.level || log.severity)}`}>
                    {(log.level || log.severity)?.toUpperCase()}
                  </td>
                  <td className="px-4 py-2">{log.source || 'system'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-gray-500 p-4">No logs match the filters.</p>
        )}
      </div>
    </div>
  );
}

// 🕒 Format time
const formatTime = (timestamp) => {
  if (!timestamp || isNaN(Date.parse(timestamp))) return 'N/A';
  return new Date(timestamp).toLocaleString();
};

// 🎨 Severity-based color
const getSeverityClass = (level) => {
  switch (level?.toUpperCase()) {
    case 'CRITICAL':
      return 'text-red-600';
    case 'ERROR':
      return 'text-orange-600';
    case 'WARNING':
      return 'text-yellow-600';
    case 'INFO':
      return 'text-blue-600';
    default:
      return '';
  }
};
