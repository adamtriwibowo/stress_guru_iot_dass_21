"""
Sistem Informasi IoT untuk Uji Stress Guru Autis
Backend API dengan Flask - DASS-21 Scoring System
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Gunakan /tmp untuk database di production (Vercel), atau current directory untuk development
import os
if os.getenv('FLASK_ENV') == 'production':
    DATABASE = '/tmp/stress_test.db'
else:
    DATABASE = 'stress_test.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabel Responden
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respondents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(10) UNIQUE NOT NULL,
            name VARCHAR(100),
            age INTEGER,
            gender VARCHAR(10),
            teaching_experience INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabel DASS-21 Questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dass21_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            category VARCHAR(20) NOT NULL,
            question_number INTEGER NOT NULL
        )
    ''')
    
    # Tabel Test Results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            respondent_id INTEGER NOT NULL,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            heart_rate_test1 FLOAT,
            heart_rate_test2 FLOAT,
            temperature_test1 FLOAT,
            temperature_test2 FLOAT,
            dass21_raw_score FLOAT,
            dass21_final_score FLOAT,
            stress_category INTEGER,
            stress_level VARCHAR(20),
            answers TEXT,
            notes TEXT,
            FOREIGN KEY (respondent_id) REFERENCES respondents(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# DASS-21 Questions (Stress subscale only - 7 questions)
DASS21_STRESS_QUESTIONS = [
    {"id": 1, "text": "Saya cenderung merasa mudah gelisah", "category": "stress"},
    {"id": 2, "text": "Saya merasa sulit untuk tenang", "category": "stress"},
    {"id": 3, "text": "Saya merasa mudah tersinggung", "category": "stress"},
    {"id": 4, "text": "Saya merasa cepat marah", "category": "stress"},
    {"id": 5, "text": "Saya merasa tegang", "category": "stress"},
    {"id": 6, "text": "Saya merasa tidak sabar", "category": "stress"},
    {"id": 7, "text": "Saya merasa sulit untuk rileks", "category": "stress"}
]

# Helper function to calculate stress category
def calculate_stress_category(score):
    if score <= 14:
        return {"category": 0, "level": "Normal", "color": "#10b981", "description": "Tidak ada stress"}
    elif score <= 18:
        return {"category": 1, "level": "Mild", "color": "#f59e0b", "description": "Stress ringan"}
    elif score <= 25:
        return {"category": 2, "level": "Moderate", "color": "#f97316", "description": "Stress sedang"}
    elif score <= 33:
        return {"category": 3, "level": "Severe", "color": "#ef4444", "description": "Stress berat"}
    else:
        return {"category": 4, "level": "Extremely Severe", "color": "#dc2626", "description": "Stress sangat berat"}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_page():
    return render_template('test.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/api/respondents', methods=['GET'])
def get_respondents():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM respondents ORDER BY created_at DESC')
    respondents = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(respondents)

@app.route('/api/respondents', methods=['POST'])
def add_respondent():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO respondents (code, name, age, gender, teaching_experience) VALUES (?, ?, ?, ?, ?)',
            (data['code'], data['name'], data['age'], data['gender'], data['teaching_experience'])
        )
        conn.commit()
        return jsonify({"id": cursor.lastrowid, "message": "Responden berhasil ditambahkan"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Kode responden sudah ada"}), 400
    finally:
        conn.close()

@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify(DASS21_STRESS_QUESTIONS)

@app.route('/api/test', methods=['POST'])
def submit_test():
    data = request.json
    
    # Calculate DASS-21 score
    answers = data['answers']
    raw_score = sum(answers.values())
    
    # DASS-21 scoring: multiply by 2 to get DASS-42 equivalent
    final_score = raw_score * 2
    
    # Calculate stress category
    stress_info = calculate_stress_category(final_score)
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO test_results (
                respondent_id, heart_rate_test1, heart_rate_test2,
                temperature_test1, temperature_test2,
                dass21_raw_score, dass21_final_score,
                stress_category, stress_level, answers
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['respondent_id'],
            data.get('heart_rate_test1'),
            data.get('heart_rate_test2'),
            data.get('temperature_test1'),
            data.get('temperature_test2'),
            raw_score,
            final_score,
            stress_info['category'],
            stress_info['level'],
            json.dumps(answers)
        ))
        conn.commit()
        
        return jsonify({
            "message": "Test berhasil disimpan",
            "score": final_score,
            "category": stress_info['category'],
            "level": stress_info['level'],
            "description": stress_info['description'],
            "color": stress_info['color']
        }), 201
    finally:
        conn.close()

@app.route('/api/results', methods=['GET'])
def get_results():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tr.*, r.code, r.name, r.age, r.gender
        FROM test_results tr
        JOIN respondents r ON tr.respondent_id = r.id
        ORDER BY tr.test_date DESC
    ''')
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/results/<int:respondent_id>', methods=['GET'])
def get_respondent_results(respondent_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tr.*, r.code, r.name
        FROM test_results tr
        JOIN respondents r ON tr.respondent_id = r.id
        WHERE tr.respondent_id = ?
        ORDER BY tr.test_date DESC
    ''', (respondent_id,))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM respondents')
    total_respondents = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM test_results')
    total_tests = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT 
            stress_category,
            COUNT(*) as count,
            AVG(dass21_final_score) as avg_score
        FROM test_results
        GROUP BY stress_category
    ''')
    category_stats = [{"category": row[0], "count": row[1], "avg_score": row[2]} 
                      for row in cursor.fetchall()]
    
    cursor.execute('''
        SELECT AVG(dass21_final_score), MIN(dass21_final_score), MAX(dass21_final_score)
        FROM test_results
    ''')
    score_stats = cursor.fetchone()
    
    conn.close()
    
    return jsonify({
        "total_respondents": total_respondents,
        "total_tests": total_tests,
        "average_score": round(score_stats[0] if score_stats[0] else 0, 2),
        "min_score": score_stats[1] if score_stats[1] else 0,
        "max_score": score_stats[2] if score_stats[2] else 0,
        "category_distribution": category_stats
    })

@app.route('/api/iot/sensor', methods=['POST'])
def receive_sensor_data():
    """Endpoint untuk menerima data dari sensor IoT"""
    data = request.json
    
    # Simulate storing sensor data
    # In real implementation, this would connect to actual IoT devices
    return jsonify({
        "message": "Data sensor diterima",
        "heart_rate": data.get('heart_rate'),
        "temperature": data.get('temperature'),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    init_db()
    import os
    debug = os.getenv('FLASK_ENV') != 'production'
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Server berjalan di http://localhost:{port}")
    app.run(debug=debug, port=port, host='0.0.0.0')
