const ReviewResult = ({ result }) => {
  if (!result) return null;

  const decisionStyles = {
    BLOCK: "bg-red-100 text-red-700",
    WARN: "bg-yellow-100 text-yellow-700",
    PASS: "bg-green-100 text-green-700"
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return "bg-red-500";
    if (confidence >= 0.6) return "bg-yellow-500";
    return "bg-green-500";
  };

  const getCoverageColor = (percent) => {
    if (percent >= 80) return "bg-green-500";
    if (percent >= 50) return "bg-yellow-500";
    return "bg-gray-400";
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
      <h2 className="text-lg font-semibold mb-4">Review Result</h2>

      {/* Decision + Risk */}
      <div className="flex items-center gap-4 mb-4">
        <span
          className={`px-3 py-1 rounded-full text-sm font-semibold ${
            decisionStyles[result.decision]
          }`}
        >
          {result.decision}
        </span>

        <span className="text-gray-700 font-medium">
          Risk Score: <b>{result.risk_score}</b>
        </span>
      </div>

      {/* Analysis Coverage */}
      {result.coverage && (
        <div className="mb-6">
          <p className="text-sm font-medium mb-1">
            Analysis Coverage: {result.coverage.percent}% ({result.coverage.level})
          </p>

          <div className="h-2 w-full bg-gray-200 rounded">
            <div
              className={`h-2 rounded ${getCoverageColor(result.coverage.percent)}`}
              style={{ width: `${result.coverage.percent}%` }}
            />
          </div>

          <p className="text-xs text-gray-500 mt-1">
            {result.coverage.description}
          </p>
        </div>
      )}

      {/* Issues */}
      <h3 className="font-semibold mb-3">Issues</h3>

      {result.issues.length === 0 && (
        <p className="text-green-600 font-medium">
          No issues detected 🎉
        </p>
      )}

      <div className="space-y-4">
        {result.issues.map((issue, index) => {
          const confidence = issue.confidence ?? 0;
          const confidencePercent = Math.round(confidence * 100);

          return (
            <div
              key={index}
              className="border rounded-lg p-4 border-l-4"
              style={{
                borderLeftColor:
                  confidence >= 0.8
                    ? "#ef4444"
                    : confidence >= 0.6
                    ? "#f59e0b"
                    : "#22c55e"
              }}
            >
              <p className="font-semibold mb-1">
                [{issue.severity}] {issue.message}
              </p>

              {/* Confidence */}
              <p className="text-sm mb-1">
                <b>Confidence:</b> {confidencePercent}%
              </p>

              <div className="h-2 w-full bg-gray-200 rounded mb-2">
                <div
                  className={`h-2 rounded ${getConfidenceColor(confidence)}`}
                  style={{ width: `${confidencePercent}%` }}
                />
              </div>

              {issue.why_it_matters && (
                <p className="text-sm text-gray-700">
                  <b>Why it matters:</b> {issue.why_it_matters}
                </p>
              )}

              {issue.interview_impact && (
                <p className="text-sm text-gray-700">
                  <b>Interview impact:</b> {issue.interview_impact}
                </p>
              )}

              {issue.production_risk && (
                <p className="text-sm text-gray-700">
                  <b>Production risk:</b> {issue.production_risk}
                </p>
              )}

              {issue.long_term_risk && (
                <p className="text-sm text-gray-700">
                  <b>Long-term risk:</b> {issue.long_term_risk}
                </p>
              )}

              {issue.suggestion && (
                <p className="text-sm text-blue-700 mt-1">
                  <b>Suggestion:</b> {issue.suggestion}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ReviewResult;
