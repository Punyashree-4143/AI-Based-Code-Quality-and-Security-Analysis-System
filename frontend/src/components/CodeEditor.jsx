import { useState } from "react";
import { reviewCode } from "../services/api";

const CodeEditor = ({ onResult }) => {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const submitCode = async () => {
    // 🛑 Guard: empty input
    if (!code || !code.trim()) {
      alert("Please enter some code before submitting.");
      return;
    }

    setLoading(true);
    setError(null);

    // 🔍 DEBUG: log payload before sending
    const payload = {
      language: "python",
      context: "deployment",
      code: code
    };

    console.log("Submitting payload:", payload);

    try {
      const result = await reviewCode(payload);
      onResult(result);
    } catch (err) {
      console.error("API ERROR:", err);
      setError("Failed to analyze code. Check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Submit Code for Review</h2>

      <textarea
        rows="10"
        cols="80"
        value={code}
        placeholder="Paste your Python code here..."
        onChange={(e) => setCode(e.target.value)}
      />

      <br />

      <button onClick={submitCode} disabled={loading}>
        {loading ? "Analyzing..." : "Review Code"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: "10px" }}>
          {error}
        </p>
      )}
    </div>
  );
};

export default CodeEditor;
