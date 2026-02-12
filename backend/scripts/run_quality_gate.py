import requests
import sys
import os

API_URL = "https://ai-based-code-quality-and-security.onrender.com/api/v1/review"

project_files = []

for root, dirs, files in os.walk("."):
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

decision = result.get("decision")
score = result.get("final_score")

print(f"Decision: {decision}")
print(f"Final Score: {score}")

if decision == "BLOCK":
    print("❌ Quality Gate FAILED")
    sys.exit(1)
else:
    print("✅ Quality Gate PASSED")
