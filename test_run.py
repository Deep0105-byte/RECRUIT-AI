from agents import jd_summarizer, resume_parser, match_scorer, shortlister, interview_scheduler
from database import db  # 👈 NEW

import os

# === Initialize DB ===
db.create_db()

# === Load JD ===
with open("data/job_descriptions.csv", "r", encoding="utf-8") as f:
    jd_text = f.read()

print("\n📝 Summarizing JD...")
jd_summary = jd_summarizer.summarize_jd(jd_text)
print("✅ JD Summary:\n", jd_summary)

# === Load First Resume ===
resumes = os.listdir("data/resumes")
if not resumes:
    print("❌ No resumes found.")
    exit()

pdf_file = resumes[0]
resume_path = f"data/resumes/{pdf_file}"
print(f"\n📄 Extracting resume: {resume_path}")
resume_text = resume_parser.extract_text_from_pdf(resume_path)

# === Match Score ===
print("\n📊 Calculating match score...")
score = match_scorer.get_score(resume_text, jd_summary)
print(f"✅ Match Score: {score}%")

# === Save to DB ===
candidate_id = pdf_file.split('.')[0]
job_id = "JD01"
db.insert_match(candidate_id, job_id, score)
print("💾 Stored match result in database.")

# === Shortlist & Email ===
if shortlister.shortlist(score):
    print("🎯 Candidate is shortlisted ✅")
    email = interview_scheduler.generate_email(candidate_id, "Software Engineer")
    print("\n📧 Email:\n", email)
else:
    print("❌ Candidate not shortlisted.")
