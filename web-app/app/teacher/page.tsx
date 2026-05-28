"use client";

import { useState } from "react";

export default function TeacherDashboard() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <main className="min-h-screen bg-[#0b1120] text-white px-8 py-6">

      {/* TOP BAR */}
      <div className="flex justify-between items-center mb-10">

        <div>
          <h1 className="text-4xl font-bold text-cyan-400">
            Teacher Dashboard
          </h1>

          <p className="text-gray-400 mt-2">
            AI Powered Classroom Monitoring
          </p>
        </div>

        {/* DROPDOWN MENU */}
        <div className="relative">

          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="bg-[#1e293b] hover:bg-[#334155] px-5 py-3 rounded-xl font-semibold"
          >
            ☰ Menu
          </button>

          {menuOpen && (
            <div className="absolute right-0 mt-3 w-60 bg-[#111827] rounded-xl shadow-lg overflow-hidden border border-gray-700 z-50">

              <button className="w-full text-left px-5 py-4 hover:bg-blue-600 transition">
                📁 Export Attendance
              </button>

              <button className="w-full text-left px-5 py-4 hover:bg-red-600 transition">
                🚨 Parent Alerts
              </button>

              <button className="w-full text-left px-5 py-4 hover:bg-gray-700 transition">
                ⏻ Exit
              </button>

            </div>
          )}
        </div>
      </div>

      {/* STATS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

        <div className="bg-[#1e293b] p-8 rounded-2xl">
          <p className="text-gray-400 mb-3">Total Students</p>
          <h2 className="text-5xl font-bold">--</h2>
        </div>

        <div className="bg-[#1e293b] p-8 rounded-2xl">
          <p className="text-gray-400 mb-3">Attendance Records</p>
          <h2 className="text-5xl font-bold">--</h2>
        </div>

        <div className="bg-[#1e293b] p-8 rounded-2xl">
          <p className="text-gray-400 mb-3">Average Attention</p>
          <h2 className="text-5xl font-bold">--%</h2>
        </div>

      </div>

      {/* ACTION BUTTONS */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <button className="bg-green-600 hover:bg-green-700 p-6 rounded-2xl text-xl font-bold transition">
          🧠 Start Measuring ClassPulse
        </button>

        <button className="bg-blue-600 hover:bg-blue-700 p-6 rounded-2xl text-xl font-bold transition">
          👤 Register Student
        </button>

        <button className="bg-purple-600 hover:bg-purple-700 p-6 rounded-2xl text-xl font-bold transition">
          📋 View Attendance
        </button>

        <button className="bg-orange-600 hover:bg-orange-700 p-6 rounded-2xl text-xl font-bold transition">
          👥 View Students
        </button>

        <button className="bg-teal-600 hover:bg-teal-700 p-6 rounded-2xl text-xl font-bold transition">
          📈 View Engagement Reports
        </button>

        <button className="bg-cyan-600 hover:bg-cyan-700 p-6 rounded-2xl text-xl font-bold transition">
          📊 ClassPulse Analysis
        </button>

      </div>

      {/* FOOTER */}
      <div className="mt-16 text-center text-gray-500 text-sm">
        ClassPulse AI • Smart Classroom Monitoring System • v1.0
      </div>

    </main>
  );
}