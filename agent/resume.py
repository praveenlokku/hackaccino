import os
import PyPDF2
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def extract_text_from_pdf(pdf_path):
    """Extract raw text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text

def extract_skills(text):
    """Extract potential skills from resume text."""
    # Basic skill extraction - in a real app, you'd use a more sophisticated approach
    common_skills = [
        "python", "javascript", "java", "c++", "react", "node.js", "sql", "machine learning",
        "data analysis", "project management", "communication", "teamwork", "leadership",
        "css", "html", "git", "docker", "aws", "azure", "api", "rest", "testing"
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills

def extract_education(text):
    """Extract education information."""
    education = []
    edu_keywords = ["bachelor", "master", "phd", "degree", "university", "college", "diploma"]
    
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in edu_keywords):
            education.append(sentence.strip())
    
    return education

def parse_resume(file_path):
    """Main function to parse resume and extract structured information."""
    text = extract_text_from_pdf(file_path)
    
    # Extract basic information
    skills = extract_skills(text)
    education = extract_education(text)
    
    # For a hackathon, this basic extraction is a good starting point
    # In a production app, you'd add more sophisticated extraction
    
    return {
        "raw_text": text,
        "skills": skills,
        "education": education
    }