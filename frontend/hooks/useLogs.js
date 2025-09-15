// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\hooks\useLogs.js

import { useState, useEffect } from 'react';
import { fetchLogs } from '../utils/api';
import { getSocket } from '../utils/socket'; // ✅ Shared WebSocket

const useLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Format helper
  const formatLog = (log) => ({
    ...log,
    time: log.timestamp || new Date().toISOString(),
    message:
      log.message?.includes("Database") && log.message?.includes("Issue")
        ? "⚠️ Database Issue Detected!"
        : log.message?.includes("High Memory")
        ? "🚨 High Memory Alert!"
        : log.message || "📝 Log Entry",
  });

  useEffect(() => {
    const getInitialLogs = async () => {
      try {
        const data = await fetchLogs();
        const formatted = data.map(formatLog);
        setLogs(formatted);
      } catch (err) {
        console.error("Error fetching logs:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    getInitialLogs();

    // ✅ Setup WebSocket
    const ws = getSocket();

    ws.onopen = () => {
      console.log("✅ WebSocket connection established (logs)");
    };

    ws.onmessage = (event) => {
      try {
        const incoming = JSON.parse(event.data);
        if (incoming.type === "log") {
          const formattedLog = formatLog(incoming);
          setLogs((prev) => [formattedLog, ...prev.slice(0, 49)]); // Keep last 50 logs
        }
      } catch (err) {
        console.error("WebSocket message parse error:", err);
      }
    };

    ws.onerror = (err) => {
      console.error("❌ WebSocket error:", err);
      setError(new Error("WebSocket connection failed"));
    };

    ws.onclose = () => {
      console.warn("⚠️ WebSocket connection closed (logs)");
    };

    // ❌ Don't close shared WebSocket on unmount
  }, []);

  return { logs, loading, error };
};

export default useLogs;
