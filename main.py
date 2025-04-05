import fitz  # PyMuPDF
import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF"""
    doc = fitz.open(pdf_path)  # Correct method to open a PDF file
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_entities(text):
    """Extract entities like name, skills, email from the resume text"""
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'SKILL']}
    return entities

# Example usage:
try:
    resume_text = extract_text_from_pdf("IOS1.pdf")
    print("Extracted Resume Text: ", resume_text)  # Log the extracted text
    entities = extract_entities(resume_text)
    print("Extracted Entities: ", entities)
except Exception as e:
    print(f"An error occurred: {e}")
    print("Check if the PDF file is accessible and the spaCy model is loaded correctly.")


# Load the pre-trained SBERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_jobs(resume_text, job_descriptions):
    """Match jobs based on resume content using SBERT"""
    resume_embedding = model.encode(resume_text)
    job_scores = [(job, util.cos_sim(resume_embedding, model.encode(job))) for job in job_descriptions]
    return sorted(job_scores, key=lambda x: x[1], reverse=True)

# Example job descriptions
jobs = [
    "Software Engineer with Python and Django experience",
    "Data Scientist with NLP skills required",
    "Frontend Developer (React, JavaScript)"
]

matched_jobs = match_jobs(resume_text, jobs)
print("Matched Jobs: ", matched_jobs)

def calculate_ats_score(resume_text, job_description):
    """Calculate a basic ATS score based on keyword matches"""
    resume_keywords = resume_text.split()  # Simple word list from the resume
    job_keywords = job_description.split()  # Simple word list from the job description
    common_keywords = set(resume_keywords) & set(job_keywords)
    ats_score = len(common_keywords) / len(set(job_keywords)) * 100  # Percentage of keyword match
    return ats_score

ats_score = calculate_ats_score(resume_text, jobs[0])  # Test with the first job description
print("ATS Score: ", ats_score)

class ResumeMatchAgent:
    def __init__(self, resume_path):
        self.resume_text = extract_text_from_pdf(resume_path)
        self.entities = extract_entities(self.resume_text)
    
    def match_jobs(self, job_descriptions):
        return match_jobs(self.resume_text, job_descriptions)
    
    def calculate_ats_score(self, job_description):
        return calculate_ats_score(self.resume_text, job_description)

# Example usage:
agent = ResumeMatchAgent("IOS1.pdf")

# Get job matches
matched_jobs = agent.match_jobs(jobs)
print("Matched Jobs: ", matched_jobs)

# Get ATS score for the first job
ats_score = agent.calculate_ats_score(jobs[0])
print("ATS Score: ", ats_score)
