import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "CryptoTrace | Real-Time Crypto Fraud Attribution System",
  description: "Real-time blockchain tracing, clustering, attribution, and risk scoring.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-[#0b0f19] text-slate-100">
        {children}
      </body>
    </html>
  );
}
