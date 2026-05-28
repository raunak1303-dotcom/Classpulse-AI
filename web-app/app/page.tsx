import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0b1120] text-white flex flex-col items-center justify-center px-6">

      <h1 className="text-6xl font-bold text-cyan-400 mb-6">
        ClassPulse AI
      </h1>

      <p className="text-gray-400 text-xl text-center max-w-2xl mb-10">
        AI-powered classroom monitoring system with smart attendance,
        engagement tracking, phone detection, analytics, and parent alerts.
      </p>

      <div className="flex gap-6 flex-wrap justify-center">

        <Link href="/teacher">
          <button className="bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-2xl text-lg font-semibold transition">
            Teacher Dashboard
          </button>
        </Link>

        <Link href="/parent">
          <button className="bg-green-600 hover:bg-green-700 px-8 py-4 rounded-2xl text-lg font-semibold transition">
            Parent Dashboard
          </button>
        </Link>

        <Link href="/student">
          <button className="bg-purple-600 hover:bg-purple-700 px-8 py-4 rounded-2xl text-lg font-semibold transition">
            Student Dashboard
          </button>
        </Link>

      </div>

      <div className="mt-16 text-gray-500 text-sm">
        ClassPulse AI • Smart Classroom Monitoring System
      </div>

    </main>
  );
}