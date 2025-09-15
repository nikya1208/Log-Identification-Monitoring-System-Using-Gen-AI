// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\utils\api.js
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const fetchLogs = async () => {
  const response = await fetch(`${API_URL}/logs`);
  if (!response.ok) throw new Error('Failed to fetch logs');
  return response.json();
};

export const fetchAlerts = async () => {
  const response = await fetch(`${API_URL}/alerts`);
  if (!response.ok) throw new Error('Failed to fetch alerts');
  return response.json();
};
