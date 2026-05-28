import type { Metadata } from "next";
import "./globals.css";
import Navbar from "./components/Navbar";

export const metadata: Metadata = {
  title: "ClassPulse AI",
  description: "AI Powered Classroom Monitoring System",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-[#0b1120] text-white">
        <Navbar />
        {children}
      </body>
    </html>
  );
}