from skills_db import SKILL_ALIASES

import re

def extract_skills(text):
    text = text.lower()
    found = set()
    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias.lower()) + r'\b'
            if re.search(pattern, text):
                found.add(skill)
                break
    return found

def skill_match_score(resume_skills, jd_skills):
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    score = len(matched) / len(jd_skills) if jd_skills else 0
    return score, matched, missing

