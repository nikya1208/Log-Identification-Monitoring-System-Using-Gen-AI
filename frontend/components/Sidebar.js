// C:\Users\NIKHIL\OneDrive\Desktop\logs\frontend\components\Sidebar.js

import Link from 'next/link';

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-800 text-white min-h-screen p-5">
      <h2 className="text-lg font-semibold mb-4">Navigation</h2>
      <ul>
        <li className="mb-2"><Link href="/"><span className="hover:text-gray-400 cursor-pointer">Dashboard</span></Link></li>
        <li className="mb-2"><Link href="/logs"><span className="hover:text-gray-400 cursor-pointer">Logs</span></Link></li>
        <li><Link href="/alerts"><span className="hover:text-gray-400 cursor-pointer">Alerts</span></Link></li>
      </ul>
    </aside>
  );
}
