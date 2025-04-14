# agents/jd_summarizer.py
import subprocess

def summarize_jd(jd_text):
    prompt = f"Summarize this JD and extract required Skills, Experience, Location, Responsibilities:\n\n{jd_text}"

    try:
        result = subprocess.run(
            ["ollama", "run", "phi"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = result.stdout.decode('utf-8', errors='ignore')
        return output.strip()

    except Exception as e:
        print("❌ Error summarizing JD:", e)
        return "Summary failed"
