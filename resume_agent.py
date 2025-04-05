import PyPDF2
import spacy
import json

# Load mock jobs
with open("jobs.json") as f:
    jobs = json.load(f)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Extract text from PDF
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = " ".join([page.extract_text() for page in reader.pages])
    return text

# Extract skills using spaCy
def get_skills(text):
    doc = nlp(text)
    skills = [token.text for token in doc if token.pos_ == "NOUN"]
    return set(skills)  # Remove duplicates

# Match jobs to resume
def match_jobs(resume_text):
    resume_skills = get_skills(resume_text)
    matched_jobs = []
    for job in jobs:
        job_skills = get_skills(job["description"])
        score = len(resume_skills & job_skills) / len(job_skills) * 100
        matched_jobs.append({**job, "score": round(score, 1)})
    return sorted(matched_jobs, key=lambda x: -x["score"])[:3]  # Top 3

# Run the agent
if __name__ == "__main__":
    resume_path = input("Enter resume path (PDF): ").strip()
    resume_text = extract_text(resume_path)
    results = match_jobs(resume_text)
    print("\nTop Matches:")
    for job in results:
        print(f"{job['company']} ({job['score']}%): {job['role']}")