import random

# Skill categories
SKILL_CATEGORIES = {
    "programming": {"python", "java", "c", "c++", "c#", "javascript", "typescript", "go", "ruby", "php", "swift", "kotlin", "rust"},
    "frontend": {"html", "css", "tailwind css", "bootstrap", "react", "angular", "vue.js", "jquery"},
    "backend": {"node.js", "express.js", "django", "flask", "spring", "laravel", "asp.net", "graphql"},
    "database": {"mysql", "postgresql", "mongodb", "oracle", "sql server", "redis", "firebase"},
    "cloud_devops": {"aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", "ci/cd", "linux", "unix", "shell scripting"},
    "data_science": {"machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "openai api"},
    "tools": {"git", "jira", "confluence", "vs code", "eclipse", "intellij", "jupyter notebook"},
    "others": {"rest api", "microservices", "graphql api", "unit testing", "agile", "oop"}
}

# Templates for skills learning steps
ACTION_TEMPLATES = {
    "programming": [
        "Learn the fundamentals of {skill}.",
        "Build a small project using {skill}.",
        "Practice applying {skill} in a real scenario."
    ],
    "frontend": [
        "Learn the basics of {skill}.",
        "Create a small UI project using {skill}.",
        "Experiment with advanced features and frameworks."
    ],
    "backend": [
        "Understand core concepts of {skill}.",
        "Develop a small backend project using {skill}.",
        "Integrate it with a frontend or database for practice."
    ],
    "database": [
        "Learn the fundamentals of {skill}.",
        "Design a small database project using {skill}.",
        "Practice CRUD operations and optimization techniques."
    ],
    "cloud_devops": [
        "Learn the basics of {skill}.",
        "Deploy a small project using {skill}.",
        "Practice real-world scenarios to solidify skills."
    ],
    "data_science": [
        "Study the core concepts of {skill}.",
        "Apply {skill} in a mini-project or dataset.",
        "Experiment with real-world datasets to improve proficiency."
    ],
    "tools": [
        "Learn how to use {skill} effectively.",
        "Practice a small task or project using {skill}.",
        "Incorporate {skill} in your workflow or project."
    ],
    "others": [
        "Understand the concepts of {skill}.",
        "Apply {skill} in a practical scenario.",
        "Revise and improve based on best practices."
    ]
}

FALLBACK_MESSAGE = "No missing skills detected. Focus on strengthening your existing skills or learning advanced concepts in your domain."

def generate_skill_action_plan(missing_skills):
    """
    Generates a step-by-step action plan for only the first missing skill,
    using category-based templates. If no missing skills, returns a fallback message.

    :param missing_skills: set of missing skills
    :return: dict {skill: [steps]} or fallback string
    """
    if not missing_skills:
        return FALLBACK_MESSAGE

    # Pick the first missing skill alphabetically
    skill = sorted(missing_skills)[0].lower()

    # Find category
    category = "others"
    for cat, skills in SKILL_CATEGORIES.items():
        if skill in skills:
            category = cat
            break

    # Pick template based on category
    template = ACTION_TEMPLATES.get(category, ACTION_TEMPLATES["others"])
    steps = [step.format(skill=skill) for step in template]

    return {skill.capitalize(): steps}
