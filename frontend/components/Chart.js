// frontend/components/Chart.js

import { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';
import { getSocket } from '@/utils/socket';

export default function Chart({ data = [] }) {
  const [chartData, setChartData] = useState(data);

  useEffect(() => {
    const ws = getSocket();

    const handleMessage = (event) => {
      try {
        const log = JSON.parse(event.data);
        const level = (log.severity || log.level || '').toUpperCase();

        if (["ERROR", "CRITICAL"].includes(level)) {
          const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

          setChartData((prev) => {
            const last = prev[prev.length - 1];

            if (last && last.time === time) {
              const updated = [...prev];
              updated[updated.length - 1].errors += 1;
              return updated;
            } else {
              return [...prev, { time, errors: 1 }].slice(-10); // Keep last 10 entries
            }
          });
        }
      } catch (err) {
        console.error(" Error parsing log in Chart.js:", err);
      }
    };

    ws.addEventListener('message', handleMessage);

    return () => {
      ws.removeEventListener('message', handleMessage);
    };
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis allowDecimals={false} />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="errors"
          stroke="#ef4444"
          strokeWidth={2}
          dot={{ r: 3 }}
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
