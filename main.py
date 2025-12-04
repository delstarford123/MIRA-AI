import os
import sys
import random
import datetime
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename

# Ensure Python can find the 'script' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the Brain
try:
    from script.predict import MiraPredictor
except ImportError:
    # Fallback if running from root
    sys.path.append(os.path.join(current_dir, 'mira'))
    from script.predict import MiraPredictor

# Initialize Flask
app = Flask(__name__, template_folder='templates', static_folder='data')

# Configuration
UPLOAD_FOLDER = os.path.join(current_dir, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load AI Brain
print("--- INITIALIZING MIRA AI SERVER ---")
try:
    ai_brain = MiraPredictor()
    print(">> AI Brain Loaded Successfully.")
except Exception as e:
    print(f">> WARNING: AI Brain failed to load. {e}")
    ai_brain = None

# --- GLOBAL MOCK DATABASE (Simulating a real DB) ---
system_config = {
    'sensitivity': 0.7,
    'model_version': 'MIRA v1.0 (TensorFlow/Keras)',
    'weather_api': True,
    'alerts_enabled': True,
    'email_reports': False
}

# ----------------------
#       ROUTES
# ----------------------

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/streams')
def streams():
    """
    Renders the Streams page with dynamic status for cameras.
    In a real app, you would query your camera IP addresses here.
    """
    # Mock Live Data
    active_streams = [
        {
            'id': 'CAM-01',
            'room': 'Lecture Hall A',
            'subject': 'Mathematics (Calculus II)',
            'teacher': 'Dr. Richards',
            'status': 'LIVE',
            'engagement': random.randint(75, 95), # Simulated live score
            'condition': 'Optimal'
        },
        {
            'id': 'CAM-02',
            'room': 'Science Lab 3',
            'subject': 'Chemistry Lab',
            'teacher': 'Prof. Stone',
            'status': 'OFFLINE',
            'engagement': 0,
            'condition': 'No Signal'
        },
        {
            'id': 'CAM-03',
            'room': 'History Dept',
            'subject': 'World War I Debate',
            'teacher': 'Ms. Sarah',
            'status': 'LIVE',
            'engagement': random.randint(40, 65),
            'condition': 'Distracted'
        }
    ]
    return render_template('streams.html', streams=active_streams)

@app.route('/analytics')
def analytics():
    """
    Prepares chart data and historical logs for the Analytics page.
    """
    # 1. Weekly Chart Data (Mon-Fri)
    weekly_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    weekly_data = [random.uniform(0.6, 0.9) for _ in range(5)] # Random scores 0.6-0.9

    # 2. Subject Breakdown
    subject_labels = ['Math', 'Science', 'History', 'Lang']
    subject_data = [85, 78, 72, 88]

    # 3. Recent Session Logs
    recent_logs = [
        {'date': 'Dec 04, 09:00', 'course': 'Mathematics 101', 'teacher': 'Mr. Ben', 'score': 88, 'insight': 'Optimal learning conditions.'},
        {'date': 'Dec 04, 11:00', 'course': 'Biology Lab', 'teacher': 'Ms. Alice', 'score': 65, 'insight': 'Rainy weather impacted focus.'},
        {'date': 'Dec 03, 14:00', 'course': 'Kiswahili', 'teacher': 'Ms. Sarah', 'score': 92, 'insight': 'High engagement detected.'},
        {'date': 'Dec 03, 10:00', 'course': 'History', 'teacher': 'Mr. Kevin', 'score': 71, 'insight': 'Average participation.'},
    ]

    return render_template('analytics.html', 
                           weekly_labels=weekly_labels, 
                           weekly_data=weekly_data,
                           subject_labels=subject_labels,
                           subject_data=subject_data,
                           logs=recent_logs)

@app.route('/settings')
def settings():
    """
    Passes the current system configuration to the Settings page.
    """
    return render_template('settings.html', config=system_config)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        ext = filename.rsplit('.', 1)[1].lower()
        score, status = 0.5, "UNKNOWN"
        
        # Analyze based on file type
        try:
            if ext in ['mp4', 'avi', 'mov']:
                score, status = ai_brain.predict_engagement(video_path=filepath)
            elif ext in ['jpg', 'jpeg', 'png']:
                score, status = ai_brain.predict_engagement(image_path=filepath)
            elif ext in ['mp3', 'wav']:
                score, status = ai_brain.predict_engagement(audio_path=filepath)
        except Exception as e:
            print(f"Prediction Error: {e}")
            return jsonify({'error': str(e)}), 500
        
        rec = "Monitoring active."
        if score > 0.7: rec = "High Engagement Detected."
        elif score < 0.4: rec = "Low Engagement. Intervention advised."

        return jsonify({
            'engagement_score': float(score),
            'status_text': status,
            'recommendation': rec,
            'filename': filename
        })

@app.route('/api/monitor')
def monitor():
    # Simulate Context
    weather = random.choice(['sunny', 'rainy', 'cloudy'])
    context = {
        'day': 'monday', 'subject': 'math', 'weather_condition': weather, 
        'response_time': 'fast', 'method_of_teaching': 'interactive',
        'teacher_experience_years': 5
    }
    
    # Grab Random Video
    video_path = None
    video_dir = os.path.join(current_dir, 'data', 'video')
    if os.path.exists(video_dir):
        files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
        if files: video_path = os.path.join(video_dir, random.choice(files))

    if ai_brain:
        score, status = ai_brain.predict_engagement(tabular_data=context, video_path=video_path)
    else:
        score, status = 0.5, "OFFLINE"

    rec = "Maintain pace."
    if score < 0.4: rec = "Attention drift detected. Suggest active learning."

    return jsonify({
        'engagement_score': float(score),
        'status_text': status,
        'weather': weather,
        'recommendation': rec
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)