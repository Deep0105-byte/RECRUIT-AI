import streamlit as st
import os
from agents import jd_summarizer, resume_parser, match_scorer, shortlister, interview_scheduler
from database import db

# Initialize the database
db.create_db()

st.title("🤖 RecruitAI - Resume Shortlister & Interview Scheduler")

# ----------------------------
# Step 1: Job Description Upload
# ----------------------------

st.subheader("📄 Upload Job Description")
uploaded_jd = st.file_uploader("Upload Job Description (TXT, CSV)", type=["txt", "csv"])

if uploaded_jd is not None:
    try:
        # Read file contents (assuming UTF-8 encoded text)
        jd_text = uploaded_jd.read().decode("utf-8")
    except Exception as e:
        st.error("Error reading the file. Please ensure it is a text-based file.")
        jd_text = ""
    
    if jd_text:
        # Summarize the job description using your summarizer agent
        jd_summary = jd_summarizer.summarize_jd(jd_text)
        # Store the summary in session state so it is available later
        st.session_state['jd_summary'] = jd_summary
        
        st.success("Job description uploaded and summarized successfully!")
        st.text_area("Job Description Summary", jd_summary, height=200)
else:
    st.info("Please upload a job description file to proceed.")

# ----------------------------
# Step 2: Resume Upload & Processing
# ----------------------------

st.subheader("📄 Upload Resumes")
resumes = st.file_uploader("Upload Multiple Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

# Only proceed if resumes are uploaded and a job description summary exists
if resumes and 'jd_summary' in st.session_state:
    for uploaded_resume in resumes:
        st.markdown(f"**Processing Resume:** `{uploaded_resume.name}`")
        
        # Create a temporary directory if it doesn't exist
        temp_dir = "data/resumes"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Define the path for the temporary resume file
        temp_path = os.path.join(temp_dir, uploaded_resume.name)
        
        # Save the resume temporarily
        with open(temp_path, "wb") as f:
            f.write(uploaded_resume.read())

        # Extract text from the resume
        resume_text = resume_parser.extract_text_from_pdf(temp_path)
        
        # Calculate the matching score using the uploaded job description summary
        score = match_scorer.get_score(resume_text, st.session_state['jd_summary'])
        st.markdown(f"**Match Score for `{uploaded_resume.name}`:** `{score}%`")
        
        # Use the filename (without extension) as candidate name (adjust as needed)
        candidate_name = os.path.splitext(uploaded_resume.name)[0]
        job_id = "JD01"  # This can be made dynamic if needed
        
        # Log the result to your database
        db.insert_match(candidate_name, job_id, score)
        
        # Determine if the candidate is shortlisted based on the matching score
        if shortlister.shortlist(score):
            st.success(f"✅ Candidate **{candidate_name}** Shortlisted!")
            interview_email = interview_scheduler.generate_email(candidate_name, "Software Engineer")
            st.markdown("#### 📧 Interview Invitation Email")
            st.code(interview_email)
        else:
            st.error(f"❌ Candidate **{candidate_name}** Not Shortlisted")