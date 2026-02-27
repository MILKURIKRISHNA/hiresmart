from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

skills_list = [
    "python", "django", "flask", "machine learning",
    "sql", "html", "css", "javascript", "react"
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/demo", methods=["GET", "POST"])
def demo():
    if request.method == "POST":
        file = request.files.get("resume")

        if not file:
            return "No file selected"

        if not file.filename.lower().endswith(".pdf"):
            return "Upload only PDF file"

        try:
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted.lower()

            if text.strip() == "":
                return "This resume appears to be scanned. Text-based PDF required."

            score = 0
            found_skills = []

            for skill in skills_list:
                if skill in text:
                    found_skills.append(skill)
                    score += 10

            score = min(score, 100)

            return render_template("result.html",
                                   skills=found_skills,
                                   score=score)

        except Exception:
            return "Error reading PDF file."

    return render_template("demo.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)