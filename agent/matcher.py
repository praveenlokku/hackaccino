import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def calculate_match_score(resume_data, job_description):
    """
    Calculate a simple match score between resume and job description.
    Returns a score from 0-100.
    """
    # Extract skills from resume
    resume_skills = set(resume_data["skills"])
    
    # Simple extraction of skills from job description
    job_skills = extract_skills_from_job(job_description)
    
    # Calculate how many resume skills match job skills
    matching_skills = resume_skills.intersection(job_skills)
    
    if len(job_skills) == 0:
        return 0
    
    # Basic score is percentage of job skills found in resume
    base_score = (len(matching_skills) / len(job_skills)) * 100
    
    # Cap at 100
    return min(base_score, 100)

def extract_skills_from_job(job_text):
    """Extract likely skills from job description."""
    # Similar to resume skill extraction
    common_skills = [
        "python", "javascript", "java", "c++", "react", "node.js", "sql", "machine learning",
        "data analysis", "project management", "communication", "teamwork", "leadership",
        "css", "html", "git", "docker", "aws", "azure", "api", "rest", "testing"
    ]
    
    found_skills = []
    job_text_lower = job_text.lower()
    
    for skill in common_skills:
        if skill in job_text_lower:
            found_skills.append(skill)
    
    return set(found_skills)

def rank_jobs(resume_data, job_listings):
    """Rank job listings based on match with resume."""
    scored_jobs = []
    
    for job in job_listings:
        score = calculate_match_score(resume_data, job["description"])
        scored_jobs.append({
            "job": job,
            "match_score": score
        })
    
    # Sort by score in descending order
    return sorted(scored_jobs, key=lambda x: x["match_score"], reverse=True)