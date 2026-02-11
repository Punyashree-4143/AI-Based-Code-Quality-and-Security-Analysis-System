from fastapi import APIRouter, Request, HTTPException
from pydantic import ValidationError

from app.models.schemas import ReviewRequest
from app.core.analyzer import analyze_code
from app.core.project_analyzer import analyze_project
from app.core.deduplicator import deduplicate_issues
from app.core.scorer import calculate_risk
from app.core.decision import make_decision
from app.core.ai_reasoner import enrich_issue
from app.core.coverage import get_language_coverage
from app.core.groq_advisory import generate_groq_advisory

router = APIRouter()


@router.post("/review")
async def review_code(request: Request):

    # =================================================
    # Step 0: Parse & Validate Request
    # =================================================
    try:
        data = await request.json()
        payload = ReviewRequest(**data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid or empty JSON body")

    # =================================================
    # Step 1: Analyze Code (Single or Project Mode)
    # =================================================
    raw_issues = []

    if payload.files:
        project_results = analyze_project(payload.files, payload.language)

        for file_result in project_results:
            for issue in file_result["issues"]:
                issue["path"] = file_result["path"]
                raw_issues.append(issue)

        analysis_mode = "project"

    elif payload.code:
        raw_issues = analyze_code(payload.code, payload.language)
        analysis_mode = "single-file"

    else:
        raise HTTPException(
            status_code=422,
            detail="Either 'code' or 'files' must be provided"
        )

    # =================================================
    # Step 2: Filter Issues by Language
    # =================================================
    filtered_issues = []
    for issue in raw_issues:
        issue_language = issue.get("language")
        if issue_language and issue_language != payload.language.lower():
            continue
        filtered_issues.append(issue)

    # =================================================
    # Step 3: Deduplicate Issues
    # =================================================
    deduped_issues = deduplicate_issues(filtered_issues)

    # =================================================
    # Step 4: Enrich Issues
    # =================================================
    enriched_issues = [
        enrich_issue(issue, payload.context)
        for issue in deduped_issues
    ]

    # =================================================
    # Step 5: Static Risk Scoring
    # =================================================
    static_score, metrics = calculate_risk(enriched_issues)

    # =================================================
    # Step 6: Structural Risk (Project-Level)
    # =================================================
    project_score = 0

    if analysis_mode == "project":
        # Simple structural heuristic (can refine later)
        project_score = min(40, len(enriched_issues) * 5)

    # =================================================
    # Step 7: AI Advisory (LLM - Safe Handling)
    # =================================================
    llm_advisory = None
    llm_modifier = 0
    interview_readiness = 0

    if payload.code:
        try:
            llm_response = generate_groq_advisory(
                code=payload.code,
                language=payload.language,
                context=payload.context
            )

            if isinstance(llm_response, dict):
                llm_advisory = llm_response.get("advisory")

                # 🔹 Force safe integer conversion
                try:
                    llm_modifier = int(llm_response.get("risk_modifier", 0))
                except (ValueError, TypeError):
                    llm_modifier = 0

                try:
                    interview_readiness = int(llm_response.get("readiness_score", 0))
                except (ValueError, TypeError):
                    interview_readiness = 0

                # 🔹 Clamp values for safety
                llm_modifier = max(0, min(llm_modifier, 10))
                interview_readiness = max(0, min(interview_readiness, 100))

            else:
                llm_advisory = str(llm_response)

        except Exception as e:
            # Fail-safe: LLM must never break review
            llm_advisory = f"AI advisory unavailable: {str(e)}"
            llm_modifier = 0
            interview_readiness = 0

    # =================================================
    # Step 8: Composite Weighted Scoring
    # =================================================
    final_score = int(
        0.5 * static_score +
        0.3 * project_score +
        0.2 * llm_modifier
    )

    # Clamp final score
    final_score = max(0, min(final_score, 100))

    decision, decision_trace = make_decision(final_score, enriched_issues)

    # =================================================
    # Step 9: Coverage
    # =================================================
    coverage = get_language_coverage(payload.language)

    # =================================================
    # Final Unified Response
    # =================================================
    return {
        "mode": analysis_mode,

        "risk_breakdown": {
            "static_risk": static_score,
            "structural_risk": project_score,
            "ai_modifier": llm_modifier
        },

        "final_score": final_score,
        "decision": decision,
        "decision_trace": decision_trace,

        "summary": f"{len(enriched_issues)} issue(s) detected",
        "coverage": coverage,
        "metrics": metrics,
        "issues": enriched_issues,

        "ai_section": {
            "interview_readiness": interview_readiness,
            "advisory": llm_advisory
        }
    }
