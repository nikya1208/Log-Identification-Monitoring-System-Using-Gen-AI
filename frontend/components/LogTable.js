export default function LogTable({ logs }) {
    return (
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">Time</th>
            <th className="border p-2">Log Message</th>
            <th className="border p-2">Severity</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, index) => (
            <tr key={index} className="text-center">
              <td className="border p-2">{log.time}</td>
              <td className="border p-2">{log.message}</td>
              <td className={`border p-2 ${log.severity === 'Critical' ? 'text-red-500' : log.severity === 'Warning' ? 'text-yellow-500' : ''}`}>
                {log.severity}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
  