import { useState } from "react";
import CodeEditor from "./components/CodeEditor";
import ReviewResult from "./components/ReviewResult";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Code Quality Gate</h1>
      <CodeEditor onResult={setResult} />
      <ReviewResult result={result} />
    </div>
  );
}

export default App;
