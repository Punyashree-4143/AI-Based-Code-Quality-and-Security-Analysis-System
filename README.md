# 🧠 AI Code Quality & Security Analysis System

An AI-powered code quality gate that performs static analysis, security detection, risk scoring, and architectural advisory — with CI/CD enforcement before deployment.

---

## 🚀 Live Demo

Frontend (Vercel):  
https://ai-based-code-quality-and-security.vercel.app

Backend API (Render):  
https://ai-based-code-quality-and-security.onrender.com

---

## 🔍 Features

- Static code analysis (Python)
- Project-level multi-file analysis
- Security detection (e.g., eval, hardcoded secrets)
- Risk scoring engine (Static + Structural + AI)
- AI architectural advisory
- PASS / WARN / BLOCK decision system
- GitHub Actions CI enforcement
- Protected `main` branch (quality-check required before merge)

---

## 🔐 CI/CD Enforcement

Workflow:

Feature Branch  
→ Pull Request  
→ GitHub Actions (`quality-check`)  
→  
• PASS → Merge allowed → Deployment  
• BLOCK → Merge prevented  

The `main` branch is protected and requires CI to pass before merging.

---

## ⚙ Tech Stack

- Python (FastAPI)
- GitHub Actions
- Render (Backend Deployment)
- Vercel (Frontend Deployment)
- Groq API (AI Advisory)
- AST-based Static Analysis

---


## **🚀 Production Deployment – Live Analysis Result**

## 🔎 Single File Code Review – Live Output

![Screenshot_12-2-2026_16433_ai-based-code-quality-and-security vercel app](https://github.com/user-attachments/assets/981e49ba-fd56-4884-bacb-acd3419af210)

## 📦 Project-Level Code Review – Live Output

![Screenshot_12-2-2026_161447_ai-based-code-quality-and-security vercel app](https://github.com/user-attachments/assets/c149a405-205d-4706-a63d-44b1881fc34d)

---
## 🧪 Run Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

