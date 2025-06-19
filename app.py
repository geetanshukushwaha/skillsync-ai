import os
import re
from typing import List, Tuple
import fitz  # PyMuPDF
import requests
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

load_dotenv()

# Configuration
LMM_API_KEY = os.getenv("GROQ_API_KEY")
LMM_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
LMM_MODEL = "llama3-8b-8192"

# Flask setup
app = Flask(__name__)
app.secret_key = "resume_match_secret_key"

# PDF extraction
def extract_text_from_pdf(file_storage) -> str:
    data = file_storage.read()
    doc = fitz.open(stream=data, filetype="pdf")
    text = "".join(page.get_text() for page in doc)
    doc.close()
    return text

# LLM call
def call_llm_for_match(resume_text: str, jd_text: str) -> Tuple[int, List[str]]:
    print(f"🔑 GROQ_API_KEY = {LMM_API_KEY}")

    if not LMM_API_KEY:
        score = simple_keyword_score(resume_text, jd_text)
        return score, [
            "LLM key not set; used keyword overlap scoring.",
            "Set GROQ_API_KEY to get AI‑generated suggestions."
        ]

    headers = {
        "Authorization": f"Bearer {LMM_API_KEY}",
        "Content-Type": "application/json",
    }

    system_prompt = (
        """You are an AI hiring assistant evaluating candidate resumes for a **generic Software Developer** role.

Your tasks:
1. Score the resume (out of 100)
2. Summarize strengths and weaknesses in one line
3. **Suggestions:** 3 specific and helpful suggestions that:
    - Highlight what’s missing from the resume **compared to the job description** (skills, experience, tools).
    - Are practical and improve hiring chances.

Note: Don't include personal details

---

🎯 Scoring Rules:
- 80–85: Exceptional fit. Strong projects + real-world experience.
- 70–79: Great fit. Strong academic + projects, minor gaps.
- 60–69: Good fit. Some relevant content but lacks depth or clarity.
- 50–59: Weak fit. Basic skills with little applied experience.
- 35–49: Poor fit. Lacks relevance to the job.
---

📌 Evaluate Based On:
✅ Skills match (languages, frameworks, tools like Git, Docker, AWS)  
✅ Project quality (real-world, team-based, measurable outcomes)  
✅ Internships and work experience (relevant + recent)  
✅ Academic background (CS degree, GPA, relevant coursework)  
✅ Certifications, contributions, or soft skills  
❌ Penalize: vague entries, lack of quantifiable impact, unrelated info, no real project/internship experience, 
missing key skills/tools mentioned in JD

---


Your response format:

Summary:  
<1-line summary of fit – e.g., "Strong academic and project experience, but lacks real-world exposure.">

Score: <number from 35 to 85>
  

Suggestions: 
1. Mention specific tools or libraries missing from the Skills section (e.g., TensorFlow, Git).  
2. Suggest adding more outcome-focused project details or metrics.  
3. Recommend including collaborative experience or open-source work.  
4. Point out missing soft skills or certifications relevant to the job description.  
5. Highlight how to make the resume more tailored to the JD.
Do not add extra text.  

Examples:

EXAMPLES:

**Example 1**  
Resume: Only Python basics, no project or internship  
Job Description: Python, SQL, data visualization, team experience  
→  
Summary: Lacks practical and team-based experience.  
Score: 52  
Suggestions:  
1. Build at least one real-world project with data processing and SQL.  
2. Learn and mention visualization tools like Matplotlib or Power BI.  
3. Highlight any group assignments or academic collaborations.  
4. Add certifications (e.g., Coursera, Google) in DS or Python.

---

**Example 2**  
Resume: Python, React, MERN project, 1 internship, 8.1 CGPA  
Job Description: React, Node.js, team projects, REST APIs  
→  
Summary: Good alignment with core skills and project experience.  
Score: 74  
Suggestions:  
1. Add backend tech like Node.js and Express to align with the job.  
2. Emphasize teamwork or Agile tools used during the project.  
3. Include any deployment experience (e.g., Heroku, Netlify).
---

**Example 3**  
Resume: Java, Android app, 2 internships, KVPY rank, OS project  
Job Description: Java, databases, software design, Agile  
→  
Summary: Excellent mix of academic merit and project depth.  
Score: 81  
Suggestions:  
1. Mention Agile methods or tools (JIRA, Trello) used in internships.  
2. Add database skills (SQL, MongoDB) more explicitly.  
3. Clarify team size and contribution in projects.



Now evaluate the following resume:
"""
    )

    user_prompt = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}"

    payload = {
        "model": LMM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 600,
    }

    response = requests.post(LMM_ENDPOINT, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    print("\n🔹 Raw LLM Response:\n", content)
    score, summary, suggestions = parse_llm_response(content)
    return summary, score, suggestions



# LLM response parsing
def parse_llm_response(text):
    summary = ""
    score = None
    suggestions = []

    # Remove bold markers like **Summary:**
    text = text.replace("**", "").strip()

    # Extract summary
    summary_match = re.search(r"Summary:\s*(.*)", text, re.IGNORECASE)
    if summary_match:
        summary = summary_match.group(1).strip()

    # Extract score
    score_match = re.search(r"Score:\s*(\d+)", text, re.IGNORECASE)
    if score_match:
        score = int(score_match.group(1).strip())
        if not (35 <= score <= 85):  # Enforce range
            score = 0

    # Extract suggestions block
    suggestions_match = re.search(r"Suggestions:\s*(.*)", text, re.IGNORECASE | re.DOTALL)
    if suggestions_match:
        block = suggestions_match.group(1).strip()

        for line in block.splitlines():
            line = line.strip()
            if line:
                # Remove bullets/numbers like "1. ", "- ", "• "
                line = re.sub(r"^[\-\*\d\.\)\s]+", "", line)
                suggestions.append(line)

    return summary, score, suggestions[:5]  # limit to top 5 if needed





# Simple fallback
def simple_keyword_score(resume: str, jd: str) -> int:
    jd_tokens = set(re.findall(r"\w+", jd.lower()))
    resume_tokens = set(re.findall(r"\w+", resume.lower()))
    if not jd_tokens:
        return 0
    overlap = jd_tokens & resume_tokens
    return int(len(overlap) / len(jd_tokens) * 100)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resume_match", methods=["GET","POST"])
def resume_match():
    jd_text = request.form.get("job_description", "").strip()
    files = request.files.getlist("resumes")

    if not jd_text:
        flash("Please paste a job description.")
        return render_template("resume_match.html", results=None, job_description="")

    if not files:
        flash("Please upload at least one resume PDF.")
        return render_template("resume_match.html", results=None, job_description=jd_text)

    results = []
    for file_storage in files:
        if file_storage and file_storage.filename.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_storage)
            try:
                score, summary, suggestions = call_llm_for_match(resume_text, jd_text)
                results.append((file_storage.filename, score, summary, suggestions))
            except Exception as e:
                flash(f"Error processing {file_storage.filename}: {str(e)}")
        else:
            flash(f"{file_storage.filename} is not a PDF and was skipped.")

    return render_template("resume_match.html", results=results, job_description=jd_text)

# Entry
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
