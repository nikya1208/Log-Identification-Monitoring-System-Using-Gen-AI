// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\pages\alerts.js

import { useState, useMemo } from 'react';
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import useAlerts from '@/hooks/useAlerts';
import { getSeverityColor } from '@/utils/helpers';

export default function Alerts() {
  const { alerts, error } = useAlerts();
  const [search, setSearch] = useState('');
  const [filterSeverity, setFilterSeverity] = useState('ALL');

  const filteredAlerts = useMemo(() => {
    return alerts.filter((alert) => {
      const matchesSearch =
        alert.message.toLowerCase().includes(search.toLowerCase()) ||
        (alert.title || '').toLowerCase().includes(search.toLowerCase());

      const matchesSeverity =
        filterSeverity === 'ALL' ||
        (alert.severity || '').toUpperCase() === filterSeverity;

      return matchesSearch && matchesSeverity;
    });
  }, [alerts, search, filterSeverity]);

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 p-6 space-y-6 overflow-hidden">
        <h2 className="text-2xl font-bold">🚨 Real-Time Alerts</h2>

        {/* Filters */}
        <div className="flex flex-wrap gap-4 items-center">
          <input
            type="text"
            placeholder="🔍 Search alerts..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border p-2 rounded-lg flex-1 min-w-[220px]"
          />
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            className="border p-2 rounded-lg"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="ERROR">Error</option>
            <option value="WARNING">Warning</option>
            <option value="INFO">Info</option>
          </select>
        </div>

        {/* Error */}
        {error && <p className="text-red-600 font-medium">{error}</p>}

        {/* Alert Table */}
        {filteredAlerts.length === 0 && !error ? (
          <p className="text-gray-500">No alerts to display.</p>
        ) : (
          <div className="overflow-auto max-h-[500px] border rounded-xl shadow-md">
            <table className="w-full text-sm text-left text-gray-800">
              <thead className="bg-gray-100 sticky top-0 z-10">
                <tr>
                  <th className="px-4 py-3">Time</th>
                  <th className="px-4 py-3">Title</th>
                  <th className="px-4 py-3">Message</th>
                  <th className="px-4 py-3">Severity</th>
                </tr>
              </thead>
              <tbody>
                {filteredAlerts.map((alert, index) => (
                  <tr
                    key={index}
                    className={`border-b hover:bg-gray-50 transition ${
                      index === 0 ? 'bg-yellow-50' : ''
                    }`}
                  >
                    <td className="px-4 py-2 whitespace-nowrap">
                      {formatTime(alert.timestamp)}
                    </td>
                    <td className="px-4 py-2">{alert.title || '—'}</td>
                    <td className="px-4 py-2">{alert.message}</td>
                    <td className="px-4 py-2">
                      <span
                        className={`text-white px-2 py-1 rounded text-xs font-semibold ${getSeverityColor(
                          alert.severity
                        )}`}
                      >
                        {alert.severity}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

// ✅ Format time consistently
const formatTime = (timestamp) => {
  try {
    return new Date(timestamp).toLocaleTimeString();
  } catch {
    return 'Invalid Time';
  }
};
