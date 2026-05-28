export default function ParentDashboard() {
  return (
    <main className="min-h-screen bg-[#0b1120] text-white px-8 py-8">
      <h1 className="text-4xl font-bold text-cyan-400 mb-2">
        Parent Dashboard
      </h1>

      <p className="text-gray-400 mb-10">
        View your child’s attendance, engagement score, and classroom activity reports.
      </p>

      <div className="bg-[#1e293b] p-8 rounded-2xl max-w-2xl">
        <h2 className="text-2xl font-bold mb-4">Student Report</h2>

        <button className="bg-green-600 hover:bg-green-700 px-6 py-4 rounded-xl font-bold mr-4">
          View Child Engagement
        </button>

        <button className="bg-purple-600 hover:bg-purple-700 px-6 py-4 rounded-xl font-bold">
          View Attendance
        </button>
      </div>
    </main>
  );
}