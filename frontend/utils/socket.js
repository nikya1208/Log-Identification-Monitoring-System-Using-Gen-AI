// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\utils\socket.js

let socket;

export const getSocket = () => {
  if (!socket || socket.readyState === WebSocket.CLOSED) {
    // ✅ Update to alerts WebSocket endpoint
    socket = new WebSocket('ws://localhost:8000/ws/alerts');

    socket.onopen = () => console.log("✅ WebSocket connected (alerts)");
    socket.onclose = () => console.warn("⚠️ WebSocket connection closed");
    socket.onerror = (e) => console.error("❌ WebSocket error:", e);
  }
  return socket;
};
