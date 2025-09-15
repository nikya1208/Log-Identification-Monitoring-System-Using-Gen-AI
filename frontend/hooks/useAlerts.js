// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\hooks\useAlerts.js

import { useEffect, useRef, useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const WS_URL = process.env.NEXT_PUBLIC_WS_ALERTS || 'ws://localhost:8000/ws/alerts';

export default function useAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState(null);

  const wsRef = useRef(null);
  const reconnectRef = useRef(true);
  const reconnectTimeout = useRef(null);

  useEffect(() => {
    if (!API_BASE || !WS_URL) {
      const errMsg = '❌ Missing API_BASE or WS_URL in .env.local';
      console.error(errMsg);
      setError(errMsg);
      return;
    }

    // Load initial alerts
    const fetchInitialAlerts = async () => {
      try {
        const res = await fetch(`${API_BASE}/alerts`);
        const data = await res.json();

        if (Array.isArray(data.alerts)) {
          setAlerts(data.alerts);
        } else if (Array.isArray(data)) {
          setAlerts(data);
        } else {
          console.warn("⚠️ Unexpected alerts format:", data);
          setError("Unexpected format from alerts endpoint.");
        }
      } catch (err) {
        console.error("❌ Failed to load initial alerts:", err);
        setError("Could not fetch alerts.");
      }
    };

    fetchInitialAlerts();

    const connectWebSocket = () => {
      try {
        const socket = new WebSocket(WS_URL);
        wsRef.current = socket;

        socket.onopen = () => {
          console.log("✅ WebSocket connected [Alerts] →", WS_URL);
        };

        socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            if (data.type === "alert") {
              setAlerts((prev) => [data, ...prev]);
            } else {
              console.warn("⚠️ Skipped non-alert WS data:", data);
            }
          } catch (err) {
            console.error("❌ Error parsing WebSocket message:", err);
          }
        };

        socket.onerror = (err) => {
          console.error("❌ WebSocket error [Alerts]:", err);
          setError("WebSocket error occurred.");
        };

        socket.onclose = (event) => {
          console.warn(`⚠️ WebSocket disconnected [Alerts] → Code: ${event.code}`);
          if (reconnectRef.current) {
            console.log("🔁 Reconnecting to alerts WebSocket in 3s...");
            reconnectTimeout.current = setTimeout(connectWebSocket, 3000);
          }
        };
      } catch (err) {
        console.error("❌ Failed to establish WebSocket connection:", err);
        setError("WebSocket connection failed.");
      }
    };

    connectWebSocket();

    return () => {
      reconnectRef.current = false;
      clearTimeout(reconnectTimeout.current);
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.close(1000, "Component unmounted");
      }
    };
  }, []);

  return { alerts, error };
}







// // C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\hooks\useAlerts.js

// import { useEffect, useRef, useState } from 'react';

// // ✅ Read env vars once
// const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;
// const WS_URL = process.env.NEXT_PUBLIC_WS_URL;

// export default function useAlerts() {
//   const [alerts, setAlerts] = useState([]);
//   const [error, setError] = useState(null);

//   const reconnectRef = useRef(true);
//   const wsRef = useRef(null);

//   useEffect(() => {
//     if (!API_BASE || !WS_URL) {
//       console.error('❌ API_BASE or WS_URL is not defined in .env.local');
//       setError('Configuration error: Missing API_BASE or WS_URL');
//       return;
//     }

//     // 📦 Load existing alerts initially
//     const fetchAlerts = async () => {
//       try {
//         const res = await fetch(`${API_BASE}/alerts`);
//         const data = await res.json();

//         if (Array.isArray(data)) {
//           setAlerts(data);
//         } else if (Array.isArray(data.alerts)) {
//           setAlerts(data.alerts);
//         } else {
//           console.warn("Unexpected alerts format:", data);
//           setError("Invalid alerts format from server.");
//         }
//       } catch (err) {
//         console.error('❌ Failed to fetch alerts:', err);
//         setError('Failed to load alerts.');
//       }
//     };

//     fetchAlerts();

//     // 🔌 WebSocket connection logic with reconnection
//     const connect = () => {
//       const ws = new WebSocket(WS_URL);
//       wsRef.current = ws;

//       ws.onopen = () => {
//         console.log('✅ WebSocket connected [Alerts]');
//       };

//       ws.onmessage = (event) => {
//         try {
//           const data = JSON.parse(event.data);
//           if (data.type !== 'alert') {
//             console.warn('[⚠️ WS skipped]', data);
//             return;
//           }

//           setAlerts((prev) => [data, ...prev]);
//         } catch (e) {
//           console.error('❌ WebSocket message parse error:', e);
//         }
//       };

//       ws.onerror = (err) => {
//         console.error('❌ WebSocket error [Alerts]:', err);
//         setError('WebSocket connection error.');
//       };

//       ws.onclose = (e) => {
//         console.warn(`⚠️ WebSocket disconnected [Alerts] → Code: ${e.code}`);
//         if (reconnectRef.current) {
//           console.log('🔁 Reconnecting in 2s...');
//           setTimeout(() => connect(), 2000);
//         }
//       };
//     };

//     connect();

//     // Cleanup on unmount
//     return () => {
//       reconnectRef.current = false;
//       wsRef.current?.close();
//     };
//   }, []);

//   return { alerts, error };
// }
