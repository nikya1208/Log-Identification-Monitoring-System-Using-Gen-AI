// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\hooks\useWebSocket.js

import { useEffect, useRef, useState } from 'react';

/**
 * useWebSocket Hook with reconnect support and exponential backoff
 * @param {string} url - WebSocket endpoint
 * @param {function} onMessage - Message handler callback
 * @param {object} [callbacks] - Optional event callbacks: onOpen, onClose, onError
 * @returns {object} WebSocket ref
 */
const useWebSocket = (url, onMessage, callbacks = {}) => {
  const wsRef = useRef(null);
  const reconnectRef = useRef(true);
  const reconnectAttempts = useRef(0);
  const [connectionStatus, setConnectionStatus] = useState('disconnected'); // Track connection status

  useEffect(() => {
    if (!url || typeof onMessage !== 'function') {
      console.warn("❌ useWebSocket: Missing URL or onMessage handler");
      return;
    }

    let reconnectTimeout;

    const connect = () => {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      // WebSocket onOpen event handler
      ws.onopen = () => {
        console.log(`✅ WebSocket connected → ${url}`);
        reconnectAttempts.current = 0; // Reset reconnect attempts after successful connection
        setConnectionStatus('connected');
        callbacks.onOpen?.(); // Optional callback for onOpen event
      };

      // WebSocket onMessage event handler
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data); // Parse the incoming message
          onMessage(data); // Pass the data to the provided message handler
        } catch (err) {
          console.error("❌ Failed to parse WebSocket message:", err);
        }
      };

      // WebSocket onError event handler
      ws.onerror = (error) => {
        console.error("❌ WebSocket error:", error);
        setConnectionStatus('error');
        callbacks.onError?.(error); // Optional callback for onError event
      };

      // WebSocket onClose event handler
      ws.onclose = (event) => {
        console.warn(`⚠️ WebSocket disconnected → Code: ${event.code}`);
        setConnectionStatus('disconnected');
        callbacks.onClose?.(event); // Optional callback for onClose event

        // Reconnect logic with exponential backoff
        if (reconnectRef.current) {
          const delay = Math.min(10000, 1000 * 2 ** reconnectAttempts.current); // Max 10s delay
          console.log(`🔄 Attempting to reconnect in ${delay / 1000}s...`);
          reconnectTimeout = setTimeout(connect, delay); // Retry connection after the calculated delay
          reconnectAttempts.current += 1; // Increment reconnect attempt counter
        }
      };
    };

    connect(); // Establish initial WebSocket connection

    // Cleanup function to run on component unmount
    return () => {
      reconnectRef.current = false; // Stop reconnecting on unmount
      reconnectAttempts.current = 0; // Reset reconnect attempts
      clearTimeout(reconnectTimeout); // Clear reconnect timeout
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.close(); // Close WebSocket if open
      }
    };
  }, [url, onMessage, callbacks]); // Dependency array: re-run effect when url or onMessage changes

  return { wsRef, connectionStatus }; // Return WebSocket reference and connection status
};

export default useWebSocket;
