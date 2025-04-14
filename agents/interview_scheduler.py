# agents/interview_scheduler.py

def generate_email(name, role):
    return f"""
Hi {name},

🎉 Congratulations!

You’ve been shortlisted for the position of **{role}**.
We would like to schedule an interview with you.

Please choose a preferred time slot:
- 10:00 AM - 10:30 AM
- 2:00 PM - 2:30 PM
- 5:00 PM - 5:30 PM

**Interview Mode**: Google Meet  
**Interviewer**: Tech Panel

Looking forward to meeting you!

Warm regards,  
RecruitAI Team
"""
