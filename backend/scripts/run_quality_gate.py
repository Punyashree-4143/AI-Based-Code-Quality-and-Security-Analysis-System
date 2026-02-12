import requests
import sys
import os
import json

API_URL = "https://ai-based-code-quality-and-security.onrender.com/api/v1/review"

project_files = []

print("\n🔎 Scanning backend/app folder only...\n")

for root, dirs, files in os.walk("app"):  # ✅ ONLY scan your code
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                project_files.append({
                    "path": path,
                    "code": f.read()
                })

payload = {
    "language": "python",
    "context": "deployment",
    "files": project_files
}

response = requests.post(API_URL, json=payload)

if response.status_code != 200:
    print("Analyzer failed.")
    sys.exit(1)

result = response.json()

print("\n==============================")
print("   QUALITY GATE REPORT")
print("==============================\n")

print("Decision:", result["decision"])
print("Final Score:", result["final_score"])

print("\nRisk Breakdown:")
print(json.dumps(result["risk_breakdown"], indent=2))

print("\nDetected Issues:\n")

for issue in result.get("issues", []):
    print(f"[{issue['severity']}] {issue['message']}")
    if "path" in issue:
        print(f"   File: {issue['path']}")
    if "suggestion" in issue:
        print(f"   Suggestion: {issue['suggestion']}")
    print()

print("\nDecision Trace:")
for reason in result.get("decision_trace", []):
    print("-", reason)

if result["decision"] == "BLOCK":
    print("\n❌ Quality Gate FAILED")
    sys.exit(1)

print("\n✅ Quality Gate PASSED")
