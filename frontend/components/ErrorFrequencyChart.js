// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\components\ErrorFrequencyChart.js

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function ErrorFrequencyChart({ data }) {
  if (!data || data.length === 0) {
    return <p className="text-gray-500">No error frequency data yet.</p>;
  }

  return (
    <div className="bg-white p-4 rounded-xl shadow border">
      <h3 className="text-xl font-semibold mb-4">📊 Error Frequency</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
