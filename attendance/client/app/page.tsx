"use client";

import Link from "next/link";

const LandingPage = () => {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[var(--color-dark)] text-[var(--color-light)] font-[var(--font-sans)] px-4">
      <h1 className="text-4xl md:text-6xl font-bold mb-4 text-center">
        Library Attendance System
      </h1>

      <p className="text-center max-w-md mb-8 text-lg">
        Scan your student QR code to record your attendance. Simple, fast, and
        paperless.
      </p>

      <Link
        href="/qr"
        className="px-8 py-4 bg-[var(--color-light)] text-[var(--color-dark)] font-semibold rounded-xl shadow-md hover:bg-gray-200 transition"
      >
        Scan QR Code
      </Link>

      <footer className="absolute bottom-6 text-sm text-gray-400">
        &copy; 2025 Library Attendance System
      </footer>
    </main>
  );
};

export default LandingPage;
