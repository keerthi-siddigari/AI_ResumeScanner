# scoring.py
from collections import Counter
import re

# Headers mapping for splitting
SECTION_HEADERS = {
    "objective": ["career objective", "objective", "summary"],
    "skills": ["technical skills", "programming languages", "skills"],
    "experience": ["projects", "experience"],
    "certifications": ["certification", "certifications"]
}

def split_resume_sections(text):
    """
    Split resume into sections based on headers.
    Returns a dict: {section_name: section_text}
    """
    sections = {k: "" for k in SECTION_HEADERS}

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    current_section = None

    for line in lines:
        line_lower = line.lower()
        matched = False
        for section, headers in SECTION_HEADERS.items():
            if any(h in line_lower for h in headers):
                current_section = section
                matched = True
                break
        if not matched and current_section:
            sections[current_section] += line + " "

    # Strip extra spaces
    for k in sections:
        sections[k] = sections[k].strip()
    return sections


def section_keyword_score(section_text, jd_keywords):
    """
    Compute 0-10 score for a section based on keyword matches.
    """
    if not section_text or not jd_keywords:
        return 0

    section_words = re.findall(r'\b\w+\b', section_text.lower())
    section_count = Counter(section_words)

    matched = sum(1 for kw in jd_keywords if kw.lower() in section_count)
    score = min((matched / len(jd_keywords)) * 10, 10)
    return round(score)


def final_score(skill_score, jd_keywords_per_section, sections):
    """
    Computes section-wise and overall resume score.
    jd_keywords_per_section: dict {section_name: list of keywords}
    """
    section_scores = {}
    for section, keywords in jd_keywords_per_section.items():
        section_scores[section] = section_keyword_score(sections.get(section, ""), keywords)

    # Weighted overall score
    weighted = (
        0.4 * (section_scores.get("skills", 0) / 10) +
        0.3 * (section_scores.get("experience", 0) / 10) +
        0.15 * (section_scores.get("certifications", 0) / 10) +
        0.15 * (section_scores.get("objective", 0) / 10)
    )
    raw = 0.6 * skill_score + 0.4 * weighted
    total_score = round(30 + raw * 70)

    return total_score, section_scores


def good_match_label(total_score):
    """
    Returns a Good Match label based on overall resume score.
    """
    if total_score >= 85:
        return "Excellent Match"
    elif total_score >= 70:
        return "Good Match"
    elif total_score >= 50:
        return "Fair Match"
    else:
        return "Poor Match"
