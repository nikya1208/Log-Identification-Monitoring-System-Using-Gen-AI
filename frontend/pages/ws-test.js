// frontend/pages/ws-test.js
import { useEffect } from "react";

export default function WebSocketLogs() {
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/logs");

    socket.onopen = () => {
      console.log("✅ Connected to WebSocket");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("📦 Received from server:", data);
    };

    socket.onclose = () => {
      console.log("❌ WebSocket disconnected");
    };

    return () => {
      socket.close();
    };
  }, []);

  return <div>🧪 Testing WebSocket – Check Console!</div>;
}
