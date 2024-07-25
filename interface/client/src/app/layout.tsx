// ------------- //
// ROOT | LAYOUT //
// ------------- //

// Imports //
import './globals.css';
import { ReactNode } from 'react';
import { Montserrat } from 'next/font/google';

// Layout Function //
const montserrat = Montserrat({ subsets: ['latin'], variable: "--font-mont" })
export default async function RootLayout({children}: {children: ReactNode}) {
  return (
    <html lang='en'>
      <body className={`${montserrat.variable} bg-light dark:bg-dark text-dark dark:text-light flex flex-col w-full min-h-screen`}>
        {children}
      </body>
    </html>
  );
};