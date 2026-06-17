import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SmartCare AI",
  description: "Smart Hospital Management System"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

