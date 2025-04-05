from .resume import parse_resume
from .matcher import rank_jobs
import requests
import json
import os

class JobMatchAgent:
    def __init__(self):
        self.resume_data = None
        self.job_cache = []
        
    def process_resume(self, resume_path):
        """Process a resume file and store the structured data."""
        self.resume_data = parse_resume(resume_path)
        return self.resume_data
    
    def fetch_jobs(self, keywords=None):
        """
        Fetch job listings from APIs or sample data.
        For hackathon, you might use sample data instead of real APIs.
        """
        # For a hackathon demo, you could use sample job data
        sample_jobs = [
            {
                "title": "Python Developer",
                "company": "TechCorp",
                "location": "Remote",
                "description": "Looking for a Python developer with experience in Flask and SQL. Must have good communication skills and teamwork.",
                "url": "https://example.com/job1"
            },
            {
                "title": "Frontend Engineer",
                "company": "WebSolutions",
                "location": "New York, NY",
                "description": "Seeking a React developer with HTML, CSS, and JavaScript experience. Knowledge of git and testing frameworks is a plus.",
                "url": "https://example.com/job2"
            },
            {
                "title": "Data Analyst",
                "company": "DataInsights",
                "location": "Chicago, IL",
                "description": "Need a data analyst with SQL and Python skills. Experience with data visualization and machine learning is preferred.",
                "url": "https://example.com/job3"
            }
        ]
        
        self.job_cache = sample_jobs
        return sample_jobs
    
    def find_matching_jobs(self):
        """Find jobs that match the parsed resume."""
        if not self.resume_data:
            raise ValueError("No resume data. Please process a resume first.")
            
        if not self.job_cache:
            self.fetch_jobs()
            
        ranked_jobs = rank_jobs(self.resume_data, self.job_cache)
        return ranked_jobs
    
    def calculate_ats_score(self):
        """
        Calculate how well the resume would perform in ATS systems.
        This is a simplified version for the hackathon.
        """
        if not self.resume_data:
            raise ValueError("No resume data. Please process a resume first.")
            
        # Simple scoring factors
        score = 70  # Base score
        
        # Add points for having skills
        if len(self.resume_data["skills"]) >= 5:
            score += 10
            
        # Add points for education
        if len(self.resume_data["education"]) > 0:
            score += 10
            
        # Add points for length of content
        if len(self.resume_data["raw_text"]) > 2000:
            score += 10
            
        return min(score, 100)  # Cap at 100