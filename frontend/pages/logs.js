// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\pages\logs.js

import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import LogsTable from '@/components/LogsTable'; // ✅ Correct component name
import useLogs from '@/hooks/useLogs';          // ✅ Real-time WebSocket logs

export default function Logs() {
  const { logs, loading, error } = useLogs();

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1 p-6 bg-gray-50">
        
        
        {/* <h2 className="text-2xl font-semibold mb-4">📜 Real-Time Logs</h2> */}

        {loading && (
          <p className="text-blue-500">Loading logs...</p>
        )}

        {error && (
          <p className="text-red-500">Error loading logs: {error.message || "WebSocket connection failed"}</p>
        )}

        {!loading && logs.length > 0 && (
          <LogsTable initialLogs={logs} />
        )}

        {!loading && logs.length === 0 && (
          <p className="text-gray-500">No logs available.</p>
        )}
      </div>
    </div>
  );
}
