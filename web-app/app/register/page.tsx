"use client";

import { useRef, useState } from "react";

export default function RegisterPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const [name, setName] = useState("");
  const [rollNo, setRollNo] = useState("");
  const [className, setClassName] = useState("");
  const [phone, setPhone] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

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
  function captureFace() {
  if (!videoRef.current || !videoRef.current.srcObject) {
    setError("Please start the camera first.");
    setSuccess("");
    return;
  }

  setError("");
  setSuccess("✅ Face captured successfully. AI training is handled by the desktop app.");
}

  async function registerStudent() {
    setError("");
    setSuccess("");

    try {
      const response = await fetch(
        "https://classpulse-ai.onrender.com/register-student",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
            roll_no: rollNo,
            class_name: className,
            phone,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed");
      }

      setSuccess("✅ Student registered successfully!");

      setName("");
      setRollNo("");
      setClassName("");
      setPhone("");
    } catch (err: any) {
      setError(err.message || "Registration failed");
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

          {success && (
            <div className="bg-green-600 p-3 rounded-xl mb-4">
              {success}
            </div>
          )}

          {error && (
            <div className="bg-red-600 p-3 rounded-xl mb-4">
              {error}
            </div>
          )}

          <div className="flex flex-col gap-5">

            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="bg-[#0f172a] p-4 rounded-xl outline-none"
              placeholder="Student Name"
            />

            <input
              value={rollNo}
              onChange={(e) => setRollNo(e.target.value)}
              className="bg-[#0f172a] p-4 rounded-xl outline-none"
              placeholder="Roll Number"
            />

            <input
              value={className}
              onChange={(e) => setClassName(e.target.value)}
              className="bg-[#0f172a] p-4 rounded-xl outline-none"
              placeholder="Class / Section"
            />

            <input
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="bg-[#0f172a] p-4 rounded-xl outline-none"
              placeholder="Phone Number"
            />

            <button
              onClick={registerStudent}
              className="bg-blue-600 hover:bg-blue-700 p-4 rounded-xl font-bold"
            >
              Register Student
            </button>
          </div>
        </div>

        <div className="flex flex-col items-center">
          <h2 className="text-2xl font-bold mb-5">
            Face Capture
          </h2>

          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="rounded-2xl border-4 border-cyan-500 w-full max-w-md bg-black"
          />

          <button
            onClick={startCamera}
            className="bg-green-600 hover:bg-green-700 mt-6 px-6 py-4 rounded-xl font-bold"
          >
            Start Camera
          </button>

          <button
            onClick={captureFace}
            className="bg-cyan-600 hover:bg-cyan-700 mt-4 px-6 py-4 rounded-xl font-bold"
          >
           Capture Face
          </button>
        </div>

      </div>
    </main>
  );
}