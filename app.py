import google.generativeai as genai
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from google.cloud import aiplatform

# # Configure Gemini API
genai.configure(api_key="AIzaSyCWwvXjCtzWn8udckd1Rb-YewwnXt66_ZU")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to parse resume using Gemini
def parse_resume_gemini(resume_text):
    model = genai.GenerativeModel("gemini-1.5-pro")  # Use Gemini model
    prompt = f"Extract structured details from this resume:\n\n{resume_text}\n\nFormat it as JSON."
    response = model.generate_content(prompt)
    return response.text  # Returns structured JSON data

# Example usage
resume_text = extract_text_from_pdf("IOS1.pdf")
parsed_data = parse_resume_gemini(resume_text)

print("Extracted Resume Data: ", parsed_data)




# Load SBERT model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to generate embeddings
def generate_embedding(text):
    return sbert_model.encode(text).tolist()  # Convert NumPy array to list for storage

# Example resume and job descriptions
resume_text = "Software Engineer with Python, Django, and AI skills."
job_descriptions = [
    "Backend Developer with Django experience",
    "AI Engineer with NLP and Deep Learning expertise",
    "Data Scientist skilled in Python and Machine Learning"
]

# Convert resume and jobs into embeddings
resume_embedding = generate_embedding(resume_text)
job_embeddings = [generate_embedding(job) for job in job_descriptions]


# Initialize Vertex AI
aiplatform.init(project="hackaccino-455606", location="us-central1")

# Create Index for Matching Engine
index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name="job-matching-index",
    dimensions=384,  # SBERT embedding size
    approximate_neighbors_count=10,
)

# Deploy the Index
index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name="job-matching-endpoint",
)

# Upload Job Embeddings
index.upsert_datapoints(
    ids=[str(i) for i in range(len(job_descriptions))],  # Unique IDs
    embeddings=job_embeddings
)

# Find similar jobs for the resume
matches = index_endpoint.match(
    deployed_index_id=index.name,
    queries=[resume_embedding],
    num_neighbors=3  # Find top 3 matches
)

# Print results
for match in matches:
    print(f"Matched Job: {job_descriptions[int(match.id)]} - Score: {match.distance}")
