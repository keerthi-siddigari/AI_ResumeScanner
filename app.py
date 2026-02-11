
from flask import Flask, render_template, request, redirect, url_for, session, flash
from preprocessing import read_pdf, preprocess
from skillsmatcher import extract_skills, skill_match_score
from scoring import split_resume_sections, final_score, good_match_label
from suggestions import generate_suggestions
from actionplan import generate_skill_action_plan
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")


@app.route('/')
def home():
    temp_path = "temp_resume.pdf"
    if os.path.exists(temp_path):
        os.remove(temp_path)

    jd_text = request.args.get('jd_text', '')
    return render_template('index.html', jd_text=jd_text)


@app.route('/scan', methods=['POST'])
def scan():
    jd_text = request.form.get('job_desc', '').strip()
    resume_file = request.files.get('resume')

    if not resume_file or not jd_text:
        error_msg = "Please upload a resume and enter a job description."
        return render_template('index.html', error=error_msg, jd_text=jd_text)

    resume_path = "temp_resume.pdf"
    resume_file.save(resume_path)
    resume_text = read_pdf(resume_path).lower()

    required_keywords = ["experience", "education", "skills", "projects"]
    if not any(word in resume_text for word in required_keywords):
        error_msg = "It seems this PDF is not a resume. Please upload a valid resume."
        flash(error_msg)
        return redirect(url_for('home', jd_text=jd_text))

    clean_resume = preprocess(resume_text)
    clean_jd = preprocess(jd_text)

    resume_skills = extract_skills(clean_resume)
    jd_skills = extract_skills(clean_jd)

    skill_score, matched, missing = skill_match_score(resume_skills, jd_skills)

    sections = split_resume_sections(clean_resume)

    jd_keywords_per_section = {
        "skills": ["python", "java", "c", "html", "css", "javascript", "mysql", "mongodb", "tailwind css", "react"],
        "experience": ["projects", "full-stack", "web applications", "AI", "API integration", "backend", "frontend"],
        "certifications": ["AI", "ML", "Java", "Python", "Coursera"],
        "objective": ["software engineer", "full-stack", "developer", "intern", "aspiring"]
    }

    score, section_scores = final_score(skill_score, jd_keywords_per_section, sections)
    match_label = good_match_label(score)

    suggestions = generate_suggestions(skill_score, sections, clean_jd, clean_resume)

    action_plan = generate_skill_action_plan(missing) if missing else \
        "No missing skills detected. Focus on strengthening your existing skills."

    # -------- WHY THIS SCORE FUNCTION (Added Cleanly) --------

    def why_this_score(total_score, section_scores):
        if total_score >= 80:
            align_text = "aligns excellently"
        elif total_score >= 65:
            align_text = "aligns well"
        elif total_score >= 50:
            align_text = "has average alignment"
        else:
            align_text = "needs improvement for a better match"

        strongest_section = max(section_scores, key=section_scores.get).capitalize()
        weakest_section = min(section_scores, key=section_scores.get).capitalize()

        explanation = (
            f"Your resume {align_text} with the job description, "
            f"showing strongest alignment in the {strongest_section} section. "
            f"The weakest section appears to be {weakest_section}, "
            "which could be improved to increase your overall match."
        )
        return explanation

    why_score_text = why_this_score(score, section_scores)

    # -------- Store in Session --------

    session["results_data"] = {
        "score": score,
        "match_label": match_label,
        "section_scores": section_scores,
        "why_score_text": why_score_text,
        "matched_display": ", ".join(sorted(matched)) if matched else "None",
        "missing_display": ", ".join(sorted(missing)) if missing else "None",
        "suggestions": suggestions,
        "action_plan": action_plan,
        "jd_text": jd_text
    }

    return redirect(url_for("results"))


@app.route('/results')
def results():
    data = session.get("results_data")

    if not data:
        return redirect(url_for("home"))

    return render_template("results.html", **data)


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
