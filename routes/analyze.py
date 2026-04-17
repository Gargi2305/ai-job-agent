from fastapi import APIRouter
from models.schemas import MatchRequest
from services.skill_extraction import extract_skills_from_jd

router = APIRouter()

@router.post("/analyze")
def analyze(request: MatchRequest):
    skills = extract_skills_from_jd(request.jd)
    return {"skills": skills}