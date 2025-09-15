// frontend/pages/_app.js
import '../styles/globals.css';
import Head from 'next/head';
import Navbar from '@/components/Navbar';

export default function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>Log Monitoring System</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="Real-time log and alert monitoring dashboard" />
        <meta charSet="UTF-8" />
        <link rel="icon" href="/favicon.ico" type="image/x-icon" />
      </Head>

      <div className="min-h-screen flex flex-col bg-gray-50">
        {/* Global Navbar */}
        <Navbar />

        {/* Page Content */}
        <main className="flex-1 max-w-screen-xl mx-auto px-4 py-6">
          <Component {...pageProps} />
        </main>
      </div>
    </>
  );
}
