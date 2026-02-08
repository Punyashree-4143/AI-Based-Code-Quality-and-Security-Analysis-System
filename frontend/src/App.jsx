import { useState } from "react";
import { Routes, Route, Navigate, Link, useLocation } from "react-router-dom";

import CodeEditor from "./components/CodeEditor";
import ReviewResult from "./components/ReviewResult";
import InterviewResult from "./components/InterviewResult";
import MultiFileReview from "./components/MultiFileReview"; // 🆕 NEW

function NavLink({ to, label }) {
  const location = useLocation();
  const active = location.pathname === to;

  return (
    <Link
      to={to}
      className={`px-4 py-2 rounded-md text-sm font-semibold transition
        ${
          active
            ? "bg-blue-600 text-white"
            : "text-gray-600 hover:bg-gray-200"
        }`}
    >
      {label}
    </Link>
  );
}

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* ================= Header ================= */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-800">
            AI Code Quality Gate
          </h1>

          <nav className="flex gap-2">
            <NavLink to="/review" label="General Review" />
            <NavLink to="/project-review" label="Project Review" /> {/* 🆕 */}
            <NavLink to="/interview" label="Interview Readiness" />
          </nav>
        </div>
      </header>

      {/* ================= Main ================= */}
      <main className="max-w-7xl mx-auto px-6 py-6">
        <Routes>
          <Route path="/" element={<Navigate to="/review" />} />

          {/* -------- Single File Review -------- */}
          <Route
            path="/review"
            element={
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <CodeEditor onResult={setResult} mode="general" />
                <ReviewResult result={result} />
              </div>
            }
          />

          {/* -------- Project / Multi-file Review -------- */}
          <Route
            path="/project-review"
            element={
              <div className="bg-white rounded-lg shadow p-6">
                <MultiFileReview />
              </div>
            }
          />

          {/* -------- Interview Mode -------- */}
          <Route
            path="/interview"
            element={
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <CodeEditor onResult={setResult} mode="interview" />
                <InterviewResult result={result} />
              </div>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

export default App;
