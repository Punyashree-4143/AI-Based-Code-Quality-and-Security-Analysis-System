from fastapi import APIRouter, Request, HTTPException
from pydantic import ValidationError

from app.models.schemas import ReviewRequest
from app.core.analyzer import analyze_code
from app.core.deduplicator import deduplicate_issues   # 🔥 NEW
from app.core.scorer import calculate_risk
from app.core.decision import make_decision
from app.core.ai_reasoner import enrich_issue
from app.core.coverage import get_language_coverage

router = APIRouter()


@router.post("/review")
async def review_code(request: Request):
    try:
        data = await request.json()
        payload = ReviewRequest(**data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid or empty JSON body")

    # =================================================
    # Step 1: Analyze code (raw issues)
    # =================================================
    raw_issues = analyze_code(payload.code, payload.language)

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
    # 🔥 Step 3: Deduplicate issues (CRITICAL UPGRADE)
    # =================================================
    deduped_issues = deduplicate_issues(filtered_issues)

    # =================================================
    # Step 4: Enrich issues (reasoning + confidence)
    # =================================================
    enriched_issues = [
        enrich_issue(issue, payload.context)
        for issue in deduped_issues
    ]

    # =================================================
    # Step 5: Score & decision
    # =================================================
    risk_score, metrics = calculate_risk(enriched_issues)
    decision = make_decision(risk_score, enriched_issues)

    # =================================================
    # Step 6: Analysis coverage
    # =================================================
    coverage = get_language_coverage(payload.language)

    return {
        "decision": decision,
        "risk_score": risk_score,
        "summary": f"{len(enriched_issues)} issue(s) detected",
        "coverage": coverage,
        "metrics": metrics,
        "issues": enriched_issues
    }
