// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\components\AlertBox.js
import { AlertTriangle, Info, XCircle, CheckCircle } from 'lucide-react';

export default function AlertBox({ title, message, severity = 'info', timestamp }) {
  const baseStyle = 'flex items-start gap-3 p-4 rounded-lg shadow-md text-white';
  const iconSize = 20;

  const getColorAndIcon = () => {
    switch ((severity || '').toUpperCase()) {
      case 'CRITICAL':
      case 'ERROR':
        return { bg: 'bg-red-500', icon: <XCircle size={iconSize} /> };
      case 'WARNING':
        return { bg: 'bg-yellow-500', icon: <AlertTriangle size={iconSize} /> };
      case 'INFO':
        return { bg: 'bg-blue-500', icon: <Info size={iconSize} /> };
      case 'SUCCESS':
        return { bg: 'bg-green-500', icon: <CheckCircle size={iconSize} /> };
      default:
        return { bg: 'bg-gray-600', icon: <Info size={iconSize} /> };
    }
  };

  const { bg, icon } = getColorAndIcon();

  return (
    <div className={`${baseStyle} ${bg}`}>
      <div className="pt-1">{icon}</div>
      <div>
        {title && <p className="font-semibold">{title}</p>}
        <p className="text-sm">{message}</p>
        {timestamp && (
          <p className="text-xs mt-1 text-white/80">
            {formatTime(timestamp)}
          </p>
        )}
      </div>
    </div>
  );
}

//  Format timestamp safely
function formatTime(ts) {
  try {
    return new Date(ts).toLocaleTimeString();
  } catch {
    return 'Invalid Time';
  }
}
