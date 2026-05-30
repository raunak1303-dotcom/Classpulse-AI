"use client";

import { useEffect, useState } from "react";

type Stats = {
  totalStudents: number;
  attendanceRecords: number;
  avgAttention: number;
  lowEngagement: number;
};

type Student = {
  id: number;
  name: string;
  roll_no: string;
  class_name: string;
  phone: string;
};

type Attendance = {
  id: number;
  name: string;
  roll_no: string;
  class_name: string;
  date: string;
  time: string;
};

type Engagement = {
  id: number;
  name: string;
  date: string;
  phone_usage: number;
  attention_score: number;
  status: string;
};

export default function TeacherDashboard() {
  const [menuOpen, setMenuOpen] = useState(false);

  const [stats, setStats] = useState<Stats>({
    totalStudents: 0,
    attendanceRecords: 0,
    avgAttention: 0,
    lowEngagement: 0,
  });

  const [students, setStudents] = useState<Student[]>([]);
  const [attendance, setAttendance] = useState<Attendance[]>([]);
  const [engagements, setEngagements] = useState<Engagement[]>([]);

  useEffect(() => {
    async function loadData() {
      const statsRes = await fetch("https://classpulse-ai.onrender.com/stats");
      const studentsRes = await fetch("https://classpulse-ai.onrender.com/students");
      const attendanceRes = await fetch("https://classpulse-ai.onrender.com/attendance");
      const engagementRes = await fetch("https://classpulse-ai.onrender.com/engagement");

      setStats(await statsRes.json());
      setStudents(await studentsRes.json());
      setAttendance(await attendanceRes.json());
      setEngagements(await engagementRes.json());
    }

    loadData();
  }, []);

  function scrollTo(id: string) {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <main className="min-h-screen bg-[#0b1120] text-white px-8 py-6">
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-bold text-cyan-400">Teacher Dashboard</h1>
          <p className="text-gray-400 mt-2">AI Powered Classroom Monitoring</p>
        </div>

        <div className="relative">
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="bg-[#1e293b] hover:bg-[#334155] px-5 py-3 rounded-xl font-semibold"
          >
            ☰ Menu
          </button>

          {menuOpen && (
            <div className="absolute right-0 mt-3 w-64 bg-[#111827] rounded-xl shadow-lg overflow-hidden border border-gray-700 z-50">
              <button
                onClick={() => (window.location.href = "https://classpulse-ai.onrender.com/export-attendance")}
                className="w-full text-left px-5 py-4 hover:bg-blue-600 transition"
              >
                📁 Export Attendance
              </button>

              <button
                onClick={() => (window.location.href = "/alerts")}
                className="w-full text-left px-5 py-4 hover:bg-red-600 transition"
              >
                🚨 Parent Alerts
              </button>

              <button
                onClick={() => (window.location.href = "/")}
                className="w-full text-left px-5 py-4 hover:bg-gray-700 transition"
              >
                ⏻ Logout
              </button>
            </div>
          )}
        </div>
      </div>

      <section className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        <StatCard title="Total Students" value={stats.totalStudents} />
        <StatCard title="Attendance Records" value={stats.attendanceRecords} />
        <StatCard title="Avg Attention" value={`${stats.avgAttention}%`} />
        <StatCard title="Low Engagement" value={stats.lowEngagement} danger />
      </section>

      <section className="bg-[#1e293b] p-8 rounded-2xl mb-10">
        <h2 className="text-2xl font-bold mb-6 text-cyan-400">Quick Actions</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ActionButton color="bg-green-600 hover:bg-green-700" onClick={() => alert("Use the desktop AI app for live camera monitoring.")}>
            🧠 Start Measuring ClassPulse
          </ActionButton>

          <ActionButton color="bg-blue-600 hover:bg-blue-700" onClick={() => (window.location.href = "/register")}>
            👤 Register Student
          </ActionButton>

          <ActionButton color="bg-purple-600 hover:bg-purple-700" onClick={() => scrollTo("attendance")}>
            📋 View Attendance
          </ActionButton>

          <ActionButton color="bg-orange-600 hover:bg-orange-700" onClick={() => scrollTo("students")}>
            👥 View Students
          </ActionButton>

          <ActionButton color="bg-teal-600 hover:bg-teal-700" onClick={() => scrollTo("engagement")}>
            📈 View Engagement Reports
          </ActionButton>

          <ActionButton color="bg-cyan-600 hover:bg-cyan-700" onClick={() => scrollTo("analysis")}>
            📊 ClassPulse Analysis
          </ActionButton>
        </div>
      </section>

      <section id="analysis" className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
        <div className="bg-[#1e293b] p-8 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-cyan-400">ClassPulse Analysis</h2>
          <div className="space-y-4 text-gray-300">
            <p>📊 Average Attention: {stats.avgAttention}%</p>
            <p>🧠 Total Monitoring Sessions: {engagements.length}</p>
            <p>⚠ Low Engagement Records: {stats.lowEngagement}</p>
            <p>📈 Reports synced from ClassPulse database</p>
          </div>
        </div>

        <div className="bg-[#1e293b] p-8 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-cyan-400">Recent Alerts</h2>
          <div className="space-y-4 text-gray-300">
            {stats.lowEngagement > 0 ? (
              <p>🚨 Some students showed low engagement today.</p>
            ) : (
              <p>✅ No low engagement alerts currently.</p>
            )}
            <p>📱 Phone usage alerts will appear here.</p>
            <p>📊 Reports are synced from ClassPulse database.</p>
          </div>
        </div>
      </section>

      <DataTable
        id="students"
        title="Registered Students"
        headers={["ID", "Name", "Roll No", "Class", "Phone"]}
        emptyMessage="No students found."
        rows={students.map((s) => [s.id, s.name, s.roll_no, s.class_name, s.phone || "N/A"])}
      />

      <DataTable
        id="attendance"
        title="Attendance History"
        headers={["Student", "Roll No", "Class", "Date", "Time"]}
        emptyMessage="No attendance records found."
        rows={attendance.map((a) => [a.name, a.roll_no, a.class_name, a.date, a.time])}
      />

      <section id="engagement" className="bg-[#1e293b] p-8 rounded-2xl overflow-x-auto">
        <h2 className="text-2xl font-bold mb-6 text-cyan-400">Live Engagement Reports</h2>

        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="py-3">Student</th>
              <th className="py-3">Date</th>
              <th className="py-3">Phone Usage</th>
              <th className="py-3">Attention</th>
              <th className="py-3">Status</th>
            </tr>
          </thead>

          <tbody>
            {engagements.length === 0 ? (
              <tr>
                <td className="py-4 text-gray-400" colSpan={5}>No engagement reports found.</td>
              </tr>
            ) : (
              engagements.map((r) => (
                <tr key={r.id} className="border-b border-gray-800 hover:bg-[#273449]">
                  <td className="py-3">{r.name}</td>
                  <td className="py-3">{r.date}</td>
                  <td className="py-3">{Number(r.phone_usage).toFixed(2)}%</td>
                  <td className="py-3">{Number(r.attention_score).toFixed(2)}%</td>
                  <td className="py-3">
                    <span className={`px-3 py-1 rounded-lg ${r.status === "Acceptable" ? "bg-green-600" : "bg-red-600"}`}>
                      {r.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>

      <div className="mt-16 text-center text-gray-500 text-sm">
        ClassPulse AI • Smart Classroom Monitoring System • v1.0
      </div>
    </main>
  );
}

function StatCard({ title, value, danger = false }: { title: string; value: string | number; danger?: boolean }) {
  return (
    <div className={`${danger ? "bg-[#7f1d1d]" : "bg-[#1e293b]"} p-7 rounded-2xl`}>
      <p className="text-gray-300 mb-3">{title}</p>
      <h2 className="text-5xl font-bold">{value}</h2>
    </div>
  );
}

function ActionButton({ children, color, onClick }: { children: React.ReactNode; color: string; onClick: () => void }) {
  return (
    <button onClick={onClick} className={`${color} p-6 rounded-2xl text-xl font-bold transition`}>
      {children}
    </button>
  );
}

function DataTable({
  id,
  title,
  headers,
  rows,
  emptyMessage,
}: {
  id: string;
  title: string;
  headers: string[];
  rows: (string | number)[][];
  emptyMessage: string;
}) {
  return (
    <section id={id} className="bg-[#1e293b] p-8 rounded-2xl mb-10 overflow-x-auto">
      <h2 className="text-2xl font-bold mb-6 text-cyan-400">{title}</h2>

      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-gray-700">
            {headers.map((h) => (
              <th key={h} className="py-3">{h}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td className="py-4 text-gray-400" colSpan={headers.length}>{emptyMessage}</td>
            </tr>
          ) : (
            rows.map((row, i) => (
              <tr key={i} className="border-b border-gray-800 hover:bg-[#273449]">
                {row.map((cell, j) => (
                  <td key={j} className="py-3">{cell}</td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </section>
  );
}