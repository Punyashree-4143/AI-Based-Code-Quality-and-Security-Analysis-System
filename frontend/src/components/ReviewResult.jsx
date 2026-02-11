const ReviewResult = ({ result }) => {
  if (!result) return null;

  const decisionStyles = {
    BLOCK: "bg-red-100 text-red-700",
    WARN: "bg-yellow-100 text-yellow-700",
    PASS: "bg-green-100 text-green-700"
  };

  const breakdown = result.risk_breakdown || {};
  const readiness = result.ai_section?.interview_readiness || 0;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
      <h2 className="text-lg font-semibold mb-4">
        AI Code Quality Gate Report
      </h2>

      {/* Decision + Final Score */}
      <div className="flex items-center gap-4 mb-4">
        <span
          className={`px-3 py-1 rounded-full text-sm font-semibold ${
            decisionStyles[result.decision]
          }`}
        >
          {result.decision}
        </span>

        <span className="text-gray-700 font-medium">
          Final Risk Score: <b>{result.final_score}</b>
        </span>
      </div>

      {/* Risk Breakdown */}
      <div className="mb-6 text-sm">
        <h3 className="font-semibold mb-2">Risk Breakdown</h3>
        <p>• Static Risk: {breakdown.static_risk}</p>
        <p>• Structural Risk: {breakdown.structural_risk}</p>
        <p>• AI Advisory Impact: +{breakdown.ai_modifier}</p>
      </div>

      {/* Interview Readiness */}
      <div className="mb-6">
        <h3 className="font-semibold mb-2">Interview Readiness</h3>
        <p className="text-sm font-medium">{readiness}%</p>

        <div className="h-2 w-full bg-gray-200 rounded">
          <div
            className={`h-2 rounded ${
              readiness >= 80
                ? "bg-green-500"
                : readiness >= 50
                ? "bg-yellow-500"
                : "bg-red-500"
            }`}
            style={{ width: `${readiness}%` }}
          />
        </div>
      </div>

      {/* Issues */}
      <h3 className="font-semibold mb-3">Issues</h3>

      {result.issues.length === 0 && (
        <p className="text-green-600 font-medium">
          No issues detected 🎉
        </p>
      )}

      <div className="space-y-4">
        {result.issues.map((issue, index) => (
          <div
            key={index}
            className="border rounded-lg p-4 border-l-4 border-blue-400"
          >
            <p className="font-semibold mb-1">
              [{issue.severity}] {issue.message}
            </p>

            {issue.suggestion && (
              <p className="text-sm text-blue-700 mt-1">
                <b>Suggestion:</b> {issue.suggestion}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* AI Advisory */}
      {result.ai_section?.advisory && (
        <div className="mt-6 bg-purple-50 border border-purple-200 p-4 rounded">
          <h3 className="font-semibold mb-2">
            🧠 AI Advisory
          </h3>
          <p className="text-sm whitespace-pre-line">
            {result.ai_section.advisory}
          </p>
        </div>
      )}
    </div>
  );
};

export default ReviewResult;
