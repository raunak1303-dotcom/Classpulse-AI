import Link from "next/link";

export default function StudentDashboard() {
  return (
    <main className="min-h-screen bg-[#0b1120] text-white px-8 py-8">

      {/* HEADER */}
      <div className="mb-10">

        <h1 className="text-4xl font-bold text-cyan-400 mb-2">
          Student Dashboard
        </h1>

        <p className="text-gray-400">
          Register yourself and track your attendance and engagement performance.
        </p>

      </div>

      {/* MAIN CARD */}
      <div className="bg-[#1e293b] p-8 rounded-2xl max-w-4xl">

        <h2 className="text-2xl font-bold mb-6">
          Student Actions
        </h2>

        {/* BUTTON GRID */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          {/* REGISTER */}
          <Link href="/register">
            <button className="w-full bg-blue-600 hover:bg-blue-700 px-6 py-5 rounded-xl font-bold text-lg transition">
              👤 Register Myself
            </button>
          </Link>

          {/* ENGAGEMENT REPORT */}
          <button className="bg-purple-600 hover:bg-purple-700 px-6 py-5 rounded-xl font-bold text-lg transition">
            📈 View My Engagement Report
          </button>

          {/* ATTENDANCE */}
          <button className="bg-cyan-600 hover:bg-cyan-700 px-6 py-5 rounded-xl font-bold text-lg transition md:col-span-2">
            📋 View Attendance Records
          </button>

        </div>

      </div>

      {/* FOOTER */}
      <div className="mt-16 text-center text-gray-500 text-sm">
        ClassPulse AI • Student Monitoring Portal • v1.0
      </div>

    </main>
  );
}