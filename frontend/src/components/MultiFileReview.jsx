import React, { useState } from "react";
import axios from "axios";

// Allowed file extensions per language
const LANGUAGE_EXTENSIONS = {
  python: [".py"],
  javascript: [".js"]
};

// Severity badge colors
const severityColors = {
  CRITICAL: "bg-red-100 text-red-800",
  MEDIUM: "bg-yellow-100 text-yellow-800",
  LOW: "bg-blue-100 text-blue-800"
};

export default function MultiFileReview() {
  const [files, setFiles] = useState([]);
  const [language, setLanguage] = useState("python");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // =========================================
  // Handle multi-file upload WITH VALIDATION
  // =========================================
  const handleFileUpload = async (event) => {
    const uploadedFiles = Array.from(event.target.files);
    const allowedExts = LANGUAGE_EXTENSIONS[language];

    // ❌ Reject invalid file types
    const invalidFiles = uploadedFiles.filter(
      (file) => !allowedExts.some((ext) => file.name.endsWith(ext))
    );

    if (invalidFiles.length > 0) {
      alert(
        `These files do not match the selected language (${language}):\n\n` +
        invalidFiles.map((f) => f.name).join(", ")
      );
      return;
    }

    const projectFiles = await Promise.all(
      uploadedFiles.map(
        (file) =>
          new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = () =>
              resolve({
                path: file.name,
                code: reader.result
              });
            reader.readAsText(file);
          })
      )
    );

    setFiles(projectFiles);
    setResult(null);
    setError(null);
  };

  // =========================================
  // Call backend API
  // =========================================
  const analyzeProject = async () => {
    if (files.length === 0) {
      alert("Please upload at least one valid file");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/v1/review",
        {
          language,
          context: "deployment",
          files
        }
      );

      setResult(response.data);
    } catch (err) {
      setError("Failed to analyze project");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // =========================================
  // Helpers
  // =========================================
  const projectIssues =
    result?.issues?.filter((i) => i.path === "__project__") || [];

  const fileIssues =
    result?.issues?.filter((i) => i.path !== "__project__") || [];

  // =========================================
  // UI
  // =========================================
  return (
    <div className="max-w-5xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">🧠 AI Project Code Review</h2>

      {/* Language Selector */}
      <div className="flex items-center gap-4 mb-4">
        <div>
          <label className="font-semibold mr-2">Language:</label>
          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setFiles([]);     // reset files on language change
              setResult(null);
            }}
            className="border rounded px-3 py-1"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
          </select>
        </div>

        {language === "javascript" && (
          <span className="text-sm text-gray-500">
            ℹ Project-level analysis available for Python
          </span>
        )}
      </div>

      {/* File Upload */}
      <input
        type="file"
        multiple
        onChange={handleFileUpload}
        className="mb-4"
      />

      <div>
        <button
          onClick={analyzeProject}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {loading ? "Analyzing..." : "Analyze Project"}
        </button>
      </div>

      {/* Error */}
      {error && <p className="text-red-600 mt-3">{error}</p>}

      {/* ================= Results ================= */}
      {result && (
        <div className="mt-8 space-y-6">
          {/* Decision Banner */}
          <div
            className={`p-4 rounded font-semibold ${
              result.decision === "PASS"
                ? "bg-green-100 text-green-800"
                : result.decision === "WARN"
                ? "bg-yellow-100 text-yellow-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            Decision: {result.decision} | Risk Score: {result.risk_score}
          </div>

          {/* Project Issues */}
          {projectIssues.length > 0 && (
            <div className="bg-white p-4 rounded shadow">
              <h3 className="font-bold mb-3">📦 Project Issues</h3>
              {projectIssues.map((issue, idx) => (
                <div key={idx} className="flex items-center gap-3 mb-2">
                  <span
                    className={`px-2 py-1 text-xs rounded ${severityColors[issue.severity]}`}
                  >
                    {issue.severity}
                  </span>
                  <span>{issue.message}</span>
                </div>
              ))}
            </div>
          )}

          {/* File Issues */}
          {fileIssues.length > 0 && (
            <div className="bg-white p-4 rounded shadow">
              <h3 className="font-bold mb-3">📄 File Issues</h3>
              {fileIssues.map((issue, idx) => (
                <div key={idx} className="flex items-center gap-3 mb-2">
                  <span
                    className={`px-2 py-1 text-xs rounded ${severityColors[issue.severity]}`}
                  >
                    {issue.severity}
                  </span>
                  <span className="font-mono text-sm">{issue.path}</span>
                  <span>{issue.message}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
