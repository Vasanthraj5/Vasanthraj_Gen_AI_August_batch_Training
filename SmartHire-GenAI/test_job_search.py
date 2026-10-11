from src.search.job_search import search_jobs

profile = {
    "name": "J VASANTHRAJ",
    "target_role": "Full-Stack Developer",
    "skills": [
        "Python",
        "Java",
        "HTML5",
        "CSS3",
        "JavaScript",
        "React.js",
        "MySQL",
        "MongoDB",
        "Git",
        "GitHub",
        "Data Preprocessing",
        "Exploratory Data Analysis",
        "AI/ML concepts"
    ],
    "education": [
        {
            "institution": "Christ College of Engineering and Technology / Puducherry",
            "degree": "Bachelor of technology (Computer Science & Engineering)",
            "duration": "2023 - 2027",
            "score": "CGPA: 8.69/10"
        }
    ],
    "experience": [
        {
            "role": "Artificial Intelligence & Machine Learning Intern",
            "company": "NexGen Technology",
            "description": "Completed an Artificial Intelligence and Machine Learning internship, gaining hands-on experience in Python, data preprocessing, exploratory data analysis, and AI/ML concepts."
        }
    ]
}

results = search_jobs(profile, 5)

print("REAL GEMINI PROFILE JOB MATCHING SUCCESS")

for i, r in enumerate(results, 1):
    print(
        f"{i}. {r['title']} | "
        f"{r['company']} | "
        f"{r['location']} | "
        f"Score: {r['score']:.4f}"
    )