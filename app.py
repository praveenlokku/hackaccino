from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from agent.core import JobMatchAgent

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/resumes'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the agent
job_agent = JobMatchAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return redirect(request.url)
        
    file = request.files['resume']
    if file.filename == '':
        return redirect(request.url)
        
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the resume
        job_agent.process_resume(file_path)
        
        return redirect(url_for('results'))
        
@app.route('/results')
def results():
    if job_agent.resume_data is None:
        return redirect(url_for('index'))
        
    # Get matching jobs
    matching_jobs = job_agent.find_matching_jobs()
    
    # Get ATS score
    ats_score = job_agent.calculate_ats_score()
    
    return render_template(
        'results.html',
        jobs=matching_jobs,
        ats_score=ats_score,
        skills=job_agent.resume_data["skills"]
    )

if __name__ == '__main__':
    app.run(debug=True)