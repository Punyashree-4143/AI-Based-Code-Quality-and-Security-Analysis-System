const InterviewResult = ({ result }) => {
  if (!result) return null;

  const criticalIssues = result.issues.filter(
    (i) => i.severity === "CRITICAL"
  );

  const mediumIssues = result.issues.filter(
    (i) => i.severity === "MEDIUM"
  );

  const readinessScore = Math.max(
    100 - result.risk_score,
    0
  );

  const isReady = criticalIssues.length === 0;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
      <h2 className="text-lg font-semibold mb-4">
        Interview Readiness
      </h2>

      {/* Status */}
      <p className="mb-2">
        <b>Status:</b>{" "}
        <span
          className={`font-semibold ${
            isReady ? "text-green-600" : "text-red-600"
          }`}
        >
          {isReady ? "Interview Ready ✅" : "Not Ready ❌"}
        </span>
      </p>

      {/* Readiness Score */}
      <p className="mb-4">
        <b>Readiness Score:</b> {readinessScore}%
      </p>

      {/* Progress Bar */}
      <div className="h-2 w-full bg-gray-200 rounded mb-5">
        <div
          className={`h-2 rounded ${
            readinessScore >= 80
              ? "bg-green-500"
              : readinessScore >= 50
              ? "bg-yellow-500"
              : "bg-red-500"
          }`}
          style={{ width: `${readinessScore}%` }}
        />
      </div>

      {/* Checklist */}
      <h3 className="font-semibold mb-2">Checklist</h3>

      <ul className="space-y-1 mb-4 text-sm">
        <li>
          {criticalIssues.length === 0 ? "✅" : "❌"} No critical issues
        </li>
        <li>
          {mediumIssues.length === 0 ? "✅" : "⚠️"} No medium issues
        </li>
        <li>
          {result.coverage?.percent >= 80 ? "✅" : "⚠️"} Good language coverage
        </li>
      </ul>

      {/* Must Fix */}
      {!isReady && (
        <>
          <h3 className="font-semibold mb-2 text-red-600">
            Must Fix Before Interview
          </h3>
          <ul className="space-y-1 text-sm">
            {criticalIssues.map((issue, idx) => (
              <li key={idx}>
                ❌ {issue.message}
              </li>
            ))}
          </ul>
        </>
      )}

      {/* Ready */}
      {isReady && (
        <p className="text-green-600 font-medium">
          Your code is suitable for technical interviews 🎉
        </p>
      )}
    </div>
  );
};

export default InterviewResult;
