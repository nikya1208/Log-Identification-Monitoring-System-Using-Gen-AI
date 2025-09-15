// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\utils\helpers.js

export const getSeverityColor = (severity) => {
  if (!severity) return 'bg-gray-300';

  const level = severity.toUpperCase();

  switch (level) {
    case 'CRITICAL':
      return 'bg-red-600';
    case 'ERROR':
      return 'bg-orange-500';
    case 'WARNING':
      return 'bg-yellow-400';
    case 'INFO':
      return 'bg-blue-400';
    case 'DEBUG':
      return 'bg-indigo-400';
    case 'SUCCESS':
      return 'bg-green-500';
    default:
      return 'bg-gray-300';
  }
};
