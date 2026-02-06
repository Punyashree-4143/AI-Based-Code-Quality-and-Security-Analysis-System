const ReviewResult = ({ result }) => {
  if (!result) return null;

  const decisionColor =
    result.decision === "BLOCK"
      ? "red"
      : result.decision === "WARN"
      ? "orange"
      : "green";

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Review Result</h2>

      <p>
        <b>Decision:</b>{" "}
        <span style={{ color: decisionColor }}>
          {result.decision}
        </span>
      </p>

      <p><b>Risk Score:</b> {result.risk_score}</p>

      <h3>Issues</h3>

      {result.issues.length === 0 && (
        <p style={{ color: "green" }}>No issues detected 🎉</p>
      )}

      {result.issues.map((issue, index) => (
        <div
          key={index}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginBottom: "10px"
          }}
        >
          <p>
            <b>[{issue.severity}]</b> {issue.message}
          </p>

          {issue.why_it_matters && (
            <p><b>Why it matters:</b> {issue.why_it_matters}</p>
          )}

          {issue.interview_impact && (
            <p><b>Interview impact:</b> {issue.interview_impact}</p>
          )}

          {issue.production_risk && (
            <p><b>Production risk:</b> {issue.production_risk}</p>
          )}

          {issue.long_term_risk && (
            <p><b>Long-term risk:</b> {issue.long_term_risk}</p>
          )}

          {issue.suggestion && (
            <p><b>Suggestion:</b> {issue.suggestion}</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default ReviewResult;
