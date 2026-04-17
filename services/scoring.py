def compute_match_score(jd_skills, resume_text):
    resume_text = resume_text.lower()

    matched = []

    for skill in jd_skills:
        s = skill.lower()

        if (
            s in resume_text or
            s.replace(" ", "") in resume_text or
            s.replace(" ", "-") in resume_text
        ):
            matched.append(skill)

    if not jd_skills:
        return 0, [], jd_skills

    score = min(95, int((len(matched) / len(jd_skills)) * 100))

    missing = [skill for skill in jd_skills if skill not in matched]

    return score, matched, missing