from fastapi import APIRouter, HTTPException
from models.schemas import MatchRequest
from services.skill_extraction import extract_skills_from_jd
from services.rag import get_resume_index, retrieve_chunks
from services.scoring import compute_match_score

router = APIRouter()

@router.post("/match")
def match(request: MatchRequest):
    try:
        jd_skills = extract_skills_from_jd(request.jd)

        chunks, index = get_resume_index(request.resume)
        rel = retrieve_chunks(request.jd[:1000], chunks, index)
        context = "\n".join(rel)

        score, matched, missing = compute_match_score(jd_skills, context)

        return {
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))