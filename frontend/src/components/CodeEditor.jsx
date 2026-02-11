import { useState } from "react";
import { reviewCode } from "../services/api";

const CodeEditor = ({ onResult }) => {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [loading, setLoading] = useState(false);

  const submitCode = async () => {
    if (!code.trim()) return;

    setLoading(true);

    try {
      const payload = {
        language,
        context: "review",
        code,
      };

      const result = await reviewCode(payload);
      onResult(result);

    } catch (error) {
      console.error("Analysis failed:", error);
      alert("Analysis failed. Check backend connection or API key.");
    }

    setLoading(false);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200">
      <div className="px-4 py-3 border-b flex items-center justify-between">
        <h2 className="font-semibold text-gray-800">
          Code Review Editor
        </h2>

        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="border rounded-md px-2 py-1 text-sm bg-white"
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="c">C</option>
          <option value="cpp">C++</option>
          <option value="java">Java</option>
        </select>
      </div>

      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder={`Write your ${language} code here...`}
        className="w-full h-72 bg-gray-900 text-gray-100 font-mono text-sm p-4 outline-none resize-none placeholder-gray-400"
      />

      <div className="px-4 py-3 border-t flex justify-end">
        <button
          onClick={submitCode}
          disabled={loading}
          className={`px-5 py-2 rounded-md font-semibold text-white transition bg-blue-600 hover:bg-blue-700 ${loading && "opacity-60 cursor-not-allowed"}`}
        >
          {loading ? "Analyzing..." : "Run Analysis"}
        </button>
      </div>
    </div>
  );
};

export default CodeEditor;
