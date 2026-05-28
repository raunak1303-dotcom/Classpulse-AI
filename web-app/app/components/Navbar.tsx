import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="w-full bg-[#0f172a] border-b border-gray-800 px-8 py-4 flex justify-between items-center">
      <Link href="/">
        <h1 className="text-2xl font-bold text-cyan-400 cursor-pointer">
          ClassPulse AI
        </h1>
      </Link>

      <div className="flex gap-6 text-gray-300 font-medium">
        <Link href="/" className="hover:text-cyan-400 transition">
          Home
        </Link>

        <Link href="/teacher" className="hover:text-cyan-400 transition">
          Teacher
        </Link>

        <Link href="/parent" className="hover:text-cyan-400 transition">
          Parent
        </Link>

        <Link href="/student" className="hover:text-cyan-400 transition">
          Student
        </Link>
      </div>
    </nav>
  );
}