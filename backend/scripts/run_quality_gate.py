import requests
import sys
import json

API_URL = "https://ai-based-code-quality-and-security.onrender.com/api/v1/review"


# Read your backend code (or specific files)
with open("app/main.py", "r") as f:
    code = f.read()

payload = {
    "language": "python",
    "context": "deployment",
    "code": code
}

response = requests.post(API_URL, json=payload)

if response.status_code != 200:
    print("❌ Failed to call API")
    sys.exit(1)

data = response.json()

print("\n=== QUALITY GATE REPORT ===")
print("Decision:", data["decision"])
print("Final Score:", data["final_score"])
print("\nRisk Breakdown:")
print(json.dumps(data["risk_breakdown"], indent=2))

print("\nIssues:")
for issue in data.get("issues", []):
    print(f"- [{issue['severity']}] {issue['message']}")
    if "path" in issue:
        print(f"  File: {issue['path']}")
    print()

print("\nDecision Trace:")
for reason in data.get("decision_trace", []):
    print("-", reason)

# 🚨 Fail CI if BLOCK
if data["decision"] == "BLOCK":
    print("\n❌ Quality Gate FAILED")
    sys.exit(1)

print("\n✅ Quality Gate PASSED")
