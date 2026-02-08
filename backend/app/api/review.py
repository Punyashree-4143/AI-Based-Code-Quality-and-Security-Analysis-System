from fastapi import APIRouter, Request, HTTPException
from pydantic import ValidationError

from app.models.schemas import ReviewRequest
from app.core.analyzer import analyze_code
from app.core.project_analyzer import analyze_project   # 🔥 NEW
from app.core.deduplicator import deduplicate_issues
from app.core.scorer import calculate_risk
from app.core.decision import make_decision
from app.core.ai_reasoner import enrich_issue
from app.core.coverage import get_language_coverage

router = APIRouter()


@router.post("/review")
async def review_code(request: Request):
    # =================================================
    # Step 0: Parse & validate request
    # =================================================
    try:
        data = await request.json()
        payload = ReviewRequest(**data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid or empty JSON body")

    # =================================================
    # Step 1: Analyze code (SINGLE or PROJECT MODE)
    # =================================================
    raw_issues = []

    if payload.files:
        # -----------------------------
        # PROJECT MODE (multi-file)
        # -----------------------------
        project_results = analyze_project(payload.files, payload.language)

        # Flatten issues for scoring & decision
        for file_result in project_results:
            for issue in file_result["issues"]:
                issue["path"] = file_result["path"]
                raw_issues.append(issue)

        analysis_mode = "project"

    elif payload.code:
        # -----------------------------
        # SINGLE FILE MODE (legacy)
        # -----------------------------
        raw_issues = analyze_code(payload.code, payload.language)
        analysis_mode = "single-file"

    else:
        raise HTTPException(
            status_code=422,
            detail="Either 'code' or 'files' must be provided"
        )

    # =================================================
    # Step 2: Filter issues by language
    # =================================================
    filtered_issues = []
    for issue in raw_issues:
        issue_language = issue.get("language")
        if issue_language and issue_language != payload.language.lower():
            continue
        filtered_issues.append(issue)

    # =================================================
    # Step 3: Deduplicate issues
    # =================================================
    deduped_issues = deduplicate_issues(filtered_issues)

    # =================================================
    # Step 4: Enrich issues (AI reasoning + confidence)
    # =================================================
    enriched_issues = [
        enrich_issue(issue, payload.context)
        for issue in deduped_issues
    ]

    # =================================================
    # Step 5: Risk scoring & decision gate
    # =================================================
    risk_score, metrics = calculate_risk(enriched_issues)
    decision = make_decision(risk_score, enriched_issues)

    # =================================================
    # Step 6: Coverage reporting
    # =================================================
    coverage = get_language_coverage(payload.language)

    # =================================================
    # Final response
    # =================================================
    return {
        "mode": analysis_mode,
        "decision": decision,
        "risk_score": risk_score,
        "summary": f"{len(enriched_issues)} issue(s) detected",
        "coverage": coverage,
        "metrics": metrics,
        "issues": enriched_issues
    }
