from fastapi import APIRouter, HTTPException
from models.schemas import MatchRequest
from services.rag import get_resume_index, retrieve_chunks
from services.llm import call_llm
from utils.parsing import parse_json_response

router = APIRouter()

@router.post("/tailor-resume")
def tailor(request: MatchRequest):
    try:
        chunks, index = get_resume_index(request.resume)
        rel = retrieve_chunks(request.jd[:1000], chunks, index)
        context = "\n".join(rel)

        system = "You rewrite resume bullets to be strong, concise, and impact-driven."

        user = f"""
Rewrite resume content to better match the job description.

STRICT RULES:
- Use strong verbs: Built, Designed, Optimized, Implemented
- Focus on technical work, systems built, and impact
- Remove all filler words
- Atleast 1-2 bullets must show impact or outcome
- Keep bullets concise (1 line each)
- Do NOT include "-" or numbering in bullets
- Avoid generic phrases

Return ONLY valid JSON (no markdown, no ```json):

{{
  "summary": "...",
  "bullets": ["...", "..."]
}}

Job Description:
{request.jd[:1500]}

Relevant Resume Content:
{context}
"""

        raw = call_llm(system, user)

        try:
            parsed = parse_json_response(raw)
        except:
            parsed = {"raw_output": raw}

        return {"output": parsed}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))