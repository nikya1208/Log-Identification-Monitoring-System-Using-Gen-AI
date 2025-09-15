// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\components\AlertsTable.js

import { useState } from 'react';
import useAlerts from '@/hooks/useAlerts';

export default function AlertsTable() {
  const { alerts } = useAlerts();
  const [search, setSearch] = useState('');
  const [severityFilter, setSeverityFilter] = useState('ALL');

  const filtered = alerts.filter((alert) => {
    const matchesSearch =
      alert.message.toLowerCase().includes(search.toLowerCase()) ||
      (alert.title || '').toLowerCase().includes(search.toLowerCase());
    const matchesSeverity =
      severityFilter === 'ALL' || (alert.severity || '').toUpperCase() === severityFilter;
    return matchesSearch && matchesSeverity;
  });

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex flex-wrap gap-4 items-center">
        <input
          type="text"
          placeholder="🔍 Search alerts..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border p-2 rounded-lg flex-1"
        />
        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="border p-2 rounded-lg"
        >
          <option value="ALL">All Severities</option>
          <option value="CRITICAL">Critical</option>
          <option value="ERROR">Error</option>
          <option value="WARNING">Warning</option>
          <option value="INFO">Info</option>
        </select>
      </div>

      {/* Table */}
      <div className="overflow-auto max-h-[400px] border rounded-xl shadow">
        <table className="w-full text-sm text-left text-gray-800">
          <thead className="bg-gray-100 sticky top-0">
            <tr>
              <th className="px-4 py-2">Time</th>
              <th className="px-4 py-2">Title</th>
              <th className="px-4 py-2">Message</th>
              <th className="px-4 py-2">Severity</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((alert, index) => (
              <tr
                key={index}
                className={`border-b hover:bg-gray-50 ${index === 0 ? 'bg-yellow-50' : ''}`}
              >
                <td className="px-4 py-2">{formatTime(alert.timestamp)}</td>
                <td className="px-4 py-2">{alert.title || '-'}</td>
                <td className="px-4 py-2">{alert.message}</td>
                <td className={`px-4 py-2 font-semibold ${getSeverityColor(alert.severity)}`}>
                  {alert.severity}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

//  Time formatter fix
const formatTime = (timestamp) => {
  try {
    return new Date(timestamp).toLocaleTimeString();
  } catch {
    return 'Invalid Time';
  }
};

const getSeverityColor = (level) => {
  switch (level?.toUpperCase()) {
    case 'CRITICAL': return 'text-red-600';
    case 'ERROR': return 'text-orange-600';
    case 'WARNING': return 'text-yellow-600';
    case 'INFO': return 'text-blue-600';
    default: return '';
  }
};
