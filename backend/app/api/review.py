from fastapi import APIRouter, Request, HTTPException
from app.models.schemas import ReviewRequest
from app.core.analyzer import analyze_code
from app.core.scorer import calculate_risk
from app.core.decision import make_decision
from app.core.ai_reasoner import enrich_issue
from pydantic import ValidationError

router = APIRouter()

@router.post("/review")
async def review_code(request: Request):
    try:
        # 🔥 Read raw JSON manually (NO ambiguity)
        data = await request.json()
        payload = ReviewRequest(**data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid or empty JSON body")

    raw_issues = analyze_code(payload.code)

    enriched_issues = [
        enrich_issue(issue, payload.context)
        for issue in raw_issues
    ]

    risk_score, metrics = calculate_risk(enriched_issues)
    decision = make_decision(risk_score, enriched_issues)

    return {
        "decision": decision,
        "risk_score": risk_score,
        "summary": f"{len(enriched_issues)} issue(s) detected",
        "metrics": metrics,
        "issues": enriched_issues
    }
