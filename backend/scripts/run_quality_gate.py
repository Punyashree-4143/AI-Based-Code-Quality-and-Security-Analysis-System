import requests
import sys
import os
import json

API_URL = "https://ai-based-code-quality-and-security.onrender.com/api/v1/review"

print("\n🔎 Scanning entire backend project...\n")

project_files = []

# Ignore unwanted folders
IGNORE_DIRS = {".venv", "__pycache__", ".git"}

for root, dirs, files in os.walk("."):
    # Remove ignored directories from traversal
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)

            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    project_files.append({
                        "path": path,
                        "code": f.read()
                    })
            except Exception as e:
                print(f"⚠️ Could not read file: {path}")

payload = {
    "language": "python",
    "context": "deployment",
    "files": project_files
}

try:
    response = requests.post(API_URL, json=payload)
except Exception as e:
    print("❌ Failed to connect to analyzer API")
    sys.exit(1)

if response.status_code != 200:
    print("❌ Analyzer returned error:", response.status_code)
    sys.exit(1)

result = response.json()

print("\n==============================")
print("   QUALITY GATE REPORT")
print("==============================\n")

print("Decision:", result.get("decision"))
print("Final Score:", result.get("final_score"))

print("\nRisk Breakdown:")
print(json.dumps(result.get("risk_breakdown", {}), indent=2))

print("\nDetected Issues:\n")

issues = result.get("issues", [])

if not issues:
    print("✅ No issues detected.")
else:
    for issue in issues:
        severity = issue.get("severity")
        message = issue.get("message")
        path = issue.get("path", "N/A")

        print(f"[{severity}] {message}")
        print(f"   File: {path}")

        if issue.get("suggestion"):
            print(f"   Suggestion: {issue.get('suggestion')}")

        print()

print("\nDecision Trace:")
for reason in result.get("decision_trace", []):
    print("-", reason)

print("\n==============================\n")

# 🚨 Fail CI if BLOCK
if result.get("decision") == "BLOCK":
    print("❌ Quality Gate FAILED - Fix issues before deployment.")
    sys.exit(1)

print("✅ Quality Gate PASSED - Safe to deploy.")
