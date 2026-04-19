# def compute_match_score(jd_skills, resume_text):
#     resume_text = resume_text.lower()

#     matched = []

#     for skill in jd_skills:
#         s = skill.lower()

#         if (
#             s in resume_text or
#             s.replace(" ", "") in resume_text or
#             s.replace(" ", "-") in resume_text
#         ):
#             matched.append(skill)

#     if not jd_skills:
#         return 0, [], jd_skills

#     score = min(95, int((len(matched) / len(jd_skills)) * 100))

#     missing = [skill for skill in jd_skills if skill not in matched]

#     return score, matched, missing

def compute_match_score(jd_skills, resume_text):
    resume_text = resume_text.lower()

    # 🔥 basic synonym normalization
    synonyms = {
        "js": "javascript",
        "node": "nodejs",
        "postgres": "postgresql",
        "ml": "machine learning",
        "ai": "artificial intelligence"
    }

    def normalize(skill):
        s = skill.lower()
        return synonyms.get(s, s)

    matched = []
    weighted_score = 0

    for skill in jd_skills:
        s = normalize(skill)

        if (
            s in resume_text or
            s.replace(" ", "") in resume_text or
            s.replace(" ", "-") in resume_text
        ):
            matched.append(skill)

            # 🔥 weight important skills higher
            if skill.lower() in ["python", "java", "c++", "fastapi", "react"]:
                weighted_score += 2
            else:
                weighted_score += 1

    if not jd_skills:
        return 0, [], jd_skills

    # 🔥 smoother scoring (less harsh)
    base = weighted_score / (len(jd_skills) + 5)

    score = int(min(95, base * 100))

    missing = [skill for skill in jd_skills if skill not in matched]

    return score, matched, missing