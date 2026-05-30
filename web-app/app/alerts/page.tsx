"use client";

import { useEffect, useState } from "react";

type Alert = {
  name: string;
  date: string;
  phoneUsage: number;
  attentionScore: number;
  message: string;
};

export default function ParentAlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    async function loadAlerts() {
      try {
        const response = await fetch("http://127.0.0.1:8000/parent-alerts");
        const data = await response.json();
        setAlerts(data);
      } catch (error) {
        console.error("Failed to load alerts:", error);
      }
    }

    loadAlerts();
  }, []);

  return (
    <main className="min-h-screen bg-[#0b1120] text-white px-8 py-8">
      <h1 className="text-4xl font-bold text-cyan-400 mb-2">
        Parent Alerts
      </h1>

      <p className="text-gray-400 mb-10">
        Auto-generated alerts for students with low engagement.
      </p>

      {alerts.length === 0 ? (
        <div className="bg-[#1e293b] p-8 rounded-2xl text-gray-300">
          ✅ No low engagement alerts found.
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {alerts.map((alert, index) => (
            <div key={index} className="bg-[#1e293b] p-8 rounded-2xl">
              <h2 className="text-2xl font-bold text-red-400 mb-4">
                🚨 {alert.name}
              </h2>

              <p className="text-gray-300 mb-2">Date: {alert.date}</p>
              <p className="text-gray-300 mb-2">
                Attention Score: {Number(alert.attentionScore).toFixed(2)}%
              </p>
              <p className="text-gray-300 mb-6">
                Phone Usage: {Number(alert.phoneUsage).toFixed(2)}%
              </p>

              <div className="bg-[#0f172a] p-5 rounded-xl text-gray-200 leading-relaxed">
                {alert.message}
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}