from pydantic import BaseModel

class MatchRequest(BaseModel):
    jd: str
    resume: str


class CoverLetterRequest(BaseModel):
    jd: str
    resume: str
    candidate_name: str = "Candidate"