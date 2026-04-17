# from fastapi import APIRouter, HTTPException
# from models.schemas import CoverLetterRequest

# from services.skill_extraction import extract_skills_from_jd
# from services.rag import get_resume_index, retrieve_chunks
# from services.scoring import compute_match_score

# from routes.tailor import tailor
# from routes.cover import cover

# router = APIRouter()

# @router.post("/full-analysis")
# def full(request: CoverLetterRequest):
#     try:
#         # STEP 1: Shared computation (IMPORTANT)
#         jd_skills = extract_skills_from_jd(request.jd)

#         chunks, index = get_resume_index(request.resume)
#         rel = retrieve_chunks(request.jd[:1000], chunks, index)
#         context = "\n".join(rel)

#         # STEP 2: Match (use SAME context)
#         score, matched, missing = compute_match_score(jd_skills, context)

#         match = {
#             "match_score": score,
#             "matched_skills": matched,
#             "missing_skills": missing
#         }

#         analysis = {"skills": jd_skills}

#         # STEP 3: Tailor (reuse API)
#         tailor_response = tailor(request)

#         # STEP 4: Cover (reuse API)
#         cover_response = cover(request)

#         return {
#             "analysis": analysis,
#             "match": match,
#             "tailored_resume": tailor_response,
#             "cover_letter": cover_response["cover_letter"]
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, HTTPException
from models.schemas import CoverLetterRequest

from services.skill_extraction import extract_skills_from_jd
from services.rag import get_resume_index, retrieve_chunks
from services.scoring import compute_match_score

from routes.tailor import tailor
from routes.cover import cover

router = APIRouter()


# ✅ CORE LOGIC (used by pipeline)
def full_logic(request: CoverLetterRequest):
    # STEP 1: Shared computation
    jd_skills = extract_skills_from_jd(request.jd)

    chunks, index = get_resume_index(request.resume)
    rel = retrieve_chunks(request.jd[:1000], chunks, index)
    context = "\n".join(rel)

    # STEP 2: Match
    score, matched, missing = compute_match_score(jd_skills, context)

    match = {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }

    analysis = {"skills": jd_skills}

    # STEP 3: Tailor
    tailor_response = tailor(request)

    # STEP 4: Cover
    cover_response = cover(request)

    return {
        "analysis": analysis,
        "match": match,
        "tailored_resume": tailor_response,
        "cover_letter": cover_response["cover_letter"]
    }


# ✅ API wrapper (only for HTTP)
@router.post("/full-analysis")
def full(request: CoverLetterRequest):
    try:
        return full_logic(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))