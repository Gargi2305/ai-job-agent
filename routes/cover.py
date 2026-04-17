from fastapi import APIRouter
from models.schemas import CoverLetterRequest
from services.rag import get_resume_index, retrieve_chunks
from services.llm import call_llm

router = APIRouter()

@router.post("/cover-letter")
def cover(request: CoverLetterRequest):
    chunks, index = get_resume_index(request.resume)
    rel = retrieve_chunks(request.jd[:1000], chunks, index)
    context = "\n".join(rel)

    system = "You write concise, technical, high-impact cover letters for software engineering roles."

    user = f"""
Write a concise, strong cover letter for a software engineering role.

Guidelines:
- Keep it under 220 words
- Use a direct, professional tone (not overly formal, not generic)
- Start naturally (DO NOT force a fixed phrase)
- Focus on technical work, systems built, and impact
- Include 1–2 quantified achievements if available
- Avoid generic phrases like "I am excited", "I am writing", "Looking forward"
- Avoid filler like "collaborated with teams"
- Use strong verbs: Built, Designed, Developed, Optimized
- Ensure it sounds like a real engineer, not a template

Return ONLY the cover letter text.

Candidate: {request.candidate_name}

Job Description:
{request.jd[:1500]}

Relevant Resume Content:
{context}
"""

    letter = call_llm(system, user)

    return {"cover_letter": letter}