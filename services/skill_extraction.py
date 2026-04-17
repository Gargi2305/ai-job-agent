from services.llm import call_llm
from utils.parsing import parse_json_response

def normalize_skills(skills):
    mapping = {
        "rest apis": "APIs",
        "rest": "APIs",
        "machine learning": "ML",
        "deep learning": "ML",
        "large language models": "LLM",
        "llms": "LLM",
        "natural language processing": "NLP"
    }

    normalized = []
    for skill in skills:
        s = skill.lower().strip()
        normalized.append(mapping.get(s, skill))

    return list(set(normalized))


def extract_skills_from_jd(jd_text):
    system = "You extract ONLY clean technical skills."

    user = f"""
Extract ONLY technical skills.

STRICT RULES:
- 1–2 words max
- NO phrases

Return JSON:
{{ "skills": ["Python", "Java", "SQL", "LLM", "APIs"] }}

Job Description:
{jd_text[:3000]}
"""

    raw = call_llm(system, user)

    try:
        parsed = parse_json_response(raw)
        return normalize_skills(parsed.get("skills", []))
    except:
        return []