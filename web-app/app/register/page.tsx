"use client";

import { useRef, useState } from "react";

export default function RegisterPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [error, setError] = useState("");

  async function startCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch {
      setError("Camera permission denied or webcam not available.");
    }
  }

  return (
    <main className="min-h-screen bg-[#0b1120] text-white flex items-center justify-center px-6 py-10">
      <div className="bg-[#1e293b] p-10 rounded-2xl w-full max-w-5xl grid md:grid-cols-2 gap-10">

        <div>
          <h1 className="text-4xl font-bold text-cyan-400 mb-3">
            Student Registration
          </h1>

          <p className="text-gray-400 mb-8">
            Register student details and capture face for ClassPulse AI.
          </p>

          <div className="flex flex-col gap-5">
            <input className="bg-[#0f172a] p-4 rounded-xl outline-none" placeholder="Student Name" />
            <input className="bg-[#0f172a] p-4 rounded-xl outline-none" placeholder="Roll Number" />
            <input className="bg-[#0f172a] p-4 rounded-xl outline-none" placeholder="Class / Section" />
            <input className="bg-[#0f172a] p-4 rounded-xl outline-none" placeholder="Phone Number" />

            <button className="bg-blue-600 hover:bg-blue-700 p-4 rounded-xl font-bold">
              Register Student
            </button>
          </div>
        </div>

        <div className="flex flex-col items-center">
          <h2 className="text-2xl font-bold mb-5">Face Capture</h2>

          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="rounded-2xl border-4 border-cyan-500 w-full max-w-md bg-black"
          />

          {error && <p className="text-red-400 mt-4">{error}</p>}

          <button
            onClick={startCamera}
            className="bg-green-600 hover:bg-green-700 mt-6 px-6 py-4 rounded-xl font-bold"
          >
            Start Camera
          </button>

          <button className="bg-cyan-600 hover:bg-cyan-700 mt-4 px-6 py-4 rounded-xl font-bold">
            Capture Face
          </button>
        </div>

      </div>
    </main>
  );
}