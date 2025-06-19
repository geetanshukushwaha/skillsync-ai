# SkillSync AI

SkillSync AI is an AI-powered resume scoring and enhancement web app that analyzes resumes based on a given job description and provides actionable suggestions to improve alignment. Built using Python, Flask, and the Groq API, the project leverages advanced language models to generate smart, tailored feedback.

## 🔍 Features

* **Smart Resume Scoring**: AI-generated relevance score based on job descriptions.
* **AI-Powered Suggestions**: Personalized, section-specific improvement tips.
* **Resume Tailoring**: Helps you align your resume to specific job roles instantly.
* **Multi-Resume Support**: Upload multiple resumes to compare results.
* **Deployed**: [Visit Live App](https://skillsync-ai-5bcg.onrender.com/)

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Frontend**: HTML, CSS, JavaScript
* **AI/ML**: Groq LLM API (GPT-based)
* **Parsing**: PDF/Text extraction using `PyMuPDF (fitz)`
* **Deployment**: Render
* **Templating**: Jinja2

## 📁 Project Structure

```
SkillSync-AI/
├── app.py                  # Main Flask app
├── templates/              # HTML pages (Jinja2)
│   ├── index.html
│   └── resume_match.html
├── static/                 # Static assets
│   ├── style.css
│   └── script.js
├── requirements.txt        # Python dependencies
├── .gitignore
├── .env                    # (Ignored) API key config
```

## 🚀 How to Run Locally

1. **Clone the repo**:

   ```bash
   git clone https://github.com/geetanshukushwaha/skillsync-ai.git
   cd skillsync-ai
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** and add your Groq API key:

   ```
   GROQ_API_KEY=your_key_here
   ```

5. **Run the app**:

   ```bash
   flask run
   ```

6. Open browser: [http://localhost:5000](http://localhost:5000)

## 📦 Deployment

* Hosted for free on [Render](https://render.com/)
* Free tier used with auto spin-down enabled to conserve resources

## 📌 Limitations

* CSS responsiveness is minimal (focus is on functionality)
* Suggestions depend on LLM quality and resume formatting

## ✅ To-Do (Future Improvements)

* Add better mobile responsiveness
* Include email/contact functionality
* Enhance suggestion engine with finer-grained section detection

## 👨‍💻 Author

Made by **Geetanshu Kushwaha**
Feel free to connect via GitHub or explore more of my projects!

