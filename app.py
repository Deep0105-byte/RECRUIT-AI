# app.py

from agents import jd_summarizer, resume_parser, match_scorer, shortlister, interview_scheduler
from database import db
import os

# === Initialize DB ===
db.create_db()

# === Load and Summarize JD ===
with open("data/job_descriptions.csv", "r", encoding="utf-8") as f:
    jd_text = f.read()

print("\n📝 Summarizing JD...")
jd_summary = jd_summarizer.summarize_jd(jd_text)
print("✅ JD Summary:\n", jd_summary)

# === Process All Resumes ===
resumes = os.listdir("data/resumes")
if not resumes:
    print("❌ No resumes found.")
    exit()

for pdf_file in resumes:
    resume_path = f"data/resumes/{pdf_file}"
    print(f"\n📄 Processing: {resume_path}")

    # 1. Extract text
    resume_text = resume_parser.extract_text_from_pdf(resume_path)

    # 2. Score it
    score = match_scorer.get_score(resume_text, jd_summary)
    print(f"🔢 Match Score: {score}%")

    # 3. Save to DB
    candidate_id = pdf_file.split('.')[0]
    job_id = "JD01"
    db.insert_match(candidate_id, job_id, score)

    # 4. Shortlist
    if shortlister.shortlist(score):
        print("✅ Shortlisted!")
        email = interview_scheduler.generate_email(candidate_id, "Software Engineer")
        print("📧 Email:\n", email)
    else:
        print("❌ Not shortlisted.")

print("\n🎉 All resumes processed successfully!")
