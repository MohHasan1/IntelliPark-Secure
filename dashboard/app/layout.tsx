import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Sidebar } from "./components/Sidebar";
import { TopBar } from "./components/TopBar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "IntelliPark",
  description: "IntelliPark Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="flex min-h-screen bg-slate-950 text-slate-50">
          <Sidebar />
          <main className="flex-1">
            <div className="mx-auto flex max-w-full flex-col gap-6 px-6 py-8">
              <TopBar />
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
