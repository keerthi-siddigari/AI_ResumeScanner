from similarity import semantic_similarity

def skill_impact_suggestion(skill_score):
    """Generate suggestion based on skill score."""
    if skill_score < 0.5:
        return "Important job-related skills are not clearly emphasized, which reduces the automated skill match score."
    elif skill_score < 0.75:
        return "Some relevant skills are present but could be highlighted more prominently to improve the skill match score."
    return None  # high skill score doesn't need skill impact suggestion


def section_level_suggestion(sections, clean_jd, skill_score):
    """Generate suggestion based on weakest section alignment."""
    section_scores = {
        "Skills section": semantic_similarity(clean_jd, sections["skills"]),
        "Experience section": semantic_similarity(clean_jd, sections["experience"]),
        "Certifications section": semantic_similarity(clean_jd, sections["certifications"]),
        "Objective section": semantic_similarity(clean_jd, sections["objective"]),
    }

    # Include Skills section only if skill score is low (optional)
    if skill_score < 0.6:
        section_scores["Skills section"] = semantic_similarity(clean_jd, sections["skills"])

    weakest = min(section_scores, key=section_scores.get)
    return f"{weakest} has low alignment with the job description and should be strengthened with role-specific details."


def presentation_suggestion_dynamic(clean_resume):
    """Generate dynamic presentation suggestions based on resume content."""
    text = clean_resume.lower()

    tool_keywords = ["python", "java", "javascript", "mysql", "mongodb", "api"]
    action_verbs = ["developed", "built", "implemented", "designed", "created", "optimized"]

    # 1. Tools mentioned but not contextualized
    if any(t in text for t in tool_keywords) and not any(v in text for v in action_verbs):
        return "Mention tools and technologies inside project or experience bullet points."

    # 2. Weak bullet phrasing (no strong verbs)
    if not any(v in text for v in action_verbs):
        return "Start project and experience bullets with action verbs to clearly communicate your contributions."

    # 3. No meaningful outcomes (ignore phone numbers/emails)
    if not any(word in text for word in ["%", "improved", "increased", "reduced", "optimized"]):
        return "Highlight outcomes or results achieved in projects to improve clarity and impact."

    # 4. Fallback suggestion if everything looks good
    return "Resume looks solid. Focus on highlighting achievements with measurable outcomes."


def generate_suggestions(skill_score, sections, clean_jd, clean_resume):
    """Combine all suggestions and ensure non-empty output."""
    suggestions = []

    s1 = skill_impact_suggestion(skill_score)
    if s1:
        suggestions.append(s1)

    suggestions.append(section_level_suggestion(sections, clean_jd, skill_score))

    s3 = presentation_suggestion_dynamic(clean_resume)
    if s3:
        suggestions.append(s3)

    # Return only non-empty suggestions
    return [s for s in suggestions if s]
