// frontend/components/Navbar.js

import Link from 'next/link';
import Image from 'next/image';

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4 text-white flex justify-between items-center">
      <div className="flex items-center">
        {/* Use Next.js Image component */}
        <Image src="/logs.png" alt="App Logo" width={50} height={50} />
        <h1 className="ml-2 text-lg font-bold">Log Monitoring System</h1>
      </div>
      <ul className="flex space-x-4">
        <li>
          <Link href="/">
            <span className="hover:underline cursor-pointer">Dashboard</span>
          </Link>
        </li>
        <li>
          <Link href="/logs">
            <span className="hover:underline cursor-pointer">Logs</span>
          </Link>
        </li>
        <li>
          <Link href="/alerts">
            <span className="hover:underline cursor-pointer">Alerts</span>
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
