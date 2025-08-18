from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import os
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)

# Database setup
def init_db():
    conn = sqlite3.connect('quiz_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL,
            student_grade TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage INTEGER NOT NULL,
            time_used INTEGER NOT NULL,
            answers TEXT NOT NULL,
            incorrect_answers TEXT NOT NULL,
            submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CAT Database Quiz System</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
                padding: 40px 20px;
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 3em;
                margin-bottom: 10px;
                font-weight: 300;
            }
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            .cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin-bottom: 40px;
            }
            .card {
                background: white;
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .card h3 {
                color: #2c3e50;
                margin-bottom: 15px;
                font-size: 1.5em;
            }
            .card p {
                color: #6c757d;
                margin-bottom: 25px;
                line-height: 1.6;
            }
            .btn { 
                display: inline-block; 
                padding: 15px 30px; 
                background: linear-gradient(135deg, #007bff, #0056b3); 
                color: white; 
                text-decoration: none; 
                border-radius: 10px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .btn:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
            }
            .btn-secondary {
                background: linear-gradient(135deg, #28a745, #20c997);
            }
            .btn-secondary:hover {
                box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
            }
            .btn-notes {
                background: linear-gradient(135deg, #6f42c1, #5a32a3);
            }
            .btn-notes:hover {
                box-shadow: 0 5px 15px rgba(111, 66, 193, 0.3);
            }
            .features {
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                padding: 30px;
                color: white;
            }
            .features h2 {
                text-align: center;
                margin-bottom: 30px;
                font-size: 2em;
            }
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }
            .feature {
                text-align: center;
                padding: 20px;
            }
            .feature-icon {
                font-size: 2.5em;
                margin-bottom: 15px;
            }
            .feature h3 {
                margin-bottom: 10px;
                font-size: 1.2em;
            }
            .feature p {
                opacity: 0.9;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 CAT Database Quiz System</h1>
                <p>Grade 11 CAT - Microsoft Access Database Learning Platform</p>
            </div>
            
            <div class="cards">
                <div class="card">
                    <h3>📝 Take Quiz</h3>
                    <p>Complete the 25-question pre-assessment quiz to evaluate your database knowledge. 30-minute timed assessment with immediate feedback.</p>
                    <a href="/quiz" class="btn">Start Quiz</a>
                </div>
                
                <div class="card">
                    <h3>📚 Study Notes</h3>
                    <p>Access comprehensive, interactive notes covering all Microsoft Access database concepts. Perfect for self-study and revision.</p>
                    <a href="/notes" class="btn btn-notes">View Notes</a>
                </div>
                
                <div class="card">
                    <h3>📊 View Results</h3>
                    <p>Teachers can access the dashboard to view all student results, analyze performance, and export data for further analysis.</p>
                    <a href="/dashboard" class="btn btn-secondary">Dashboard</a>
                </div>
            </div>

            <div class="features">
                <h2>🎯 Features</h2>
                <div class="features-grid">
                    <div class="feature">
                        <div class="feature-icon">⏱️</div>
                        <h3>Timed Assessment</h3>
                        <p>30-minute quiz with real-time progress tracking</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">📱</div>
                        <h3>Mobile Responsive</h3>
                        <p>Works perfectly on desktop, tablet, and mobile devices</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">🔍</div>
                        <h3>Interactive Notes</h3>
                        <p>Searchable, collapsible content with dark/light mode</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">📊</div>
                        <h3>Detailed Analytics</h3>
                        <p>Comprehensive performance analysis and reporting</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">💾</div>
                        <h3>Data Export</h3>
                        <p>Export results to CSV for further analysis</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">🌐</div>
                        <h3>Online Access</h3>
                        <p>Access from anywhere with internet connection</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/quiz')
def quiz():
    # Serve the enhanced 25-question quiz HTML file
    with open('CAT_Grade11_Database_Quiz_25Questions_Enhanced.html', 'r', encoding='utf-8') as f:
        quiz_html = f.read()
    
    # Replace the localStorage submission with API call
    quiz_html = quiz_html.replace(
        'function submitToBackend(quizData) {',
        '''function submitToBackend(quizData) {
            // Submit to Railway backend API
            fetch('/api/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(quizData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Quiz submitted successfully');
                } else {
                    console.error('Error submitting quiz:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback to localStorage
                const submissions = JSON.parse(localStorage.getItem('quizSubmissions') || '[]');
                submissions.push(quizData);
                localStorage.setItem('quizSubmissions', JSON.stringify(submissions));
            });'''
    )
    
    return quiz_html

@app.route('/notes')
def notes():
    # Serve the enhanced notes HTML file
    with open('CAT_Database_Enhanced_Notes.html', 'r', encoding='utf-8') as f:
        notes_html = f.read()
    return notes_html

@app.route('/dashboard')
def dashboard():
    # Serve the dashboard HTML file
    with open('CAT_Grade11_Database_Dashboard.html', 'r', encoding='utf-8') as f:
        dashboard_html = f.read()
    
    # Replace localStorage loading with API call
    dashboard_html = dashboard_html.replace(
        'function loadData() {',
        '''function loadData() {
            // Load from Railway backend API
            fetch('/api/results')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    allSubmissions = data.results;
                    filteredSubmissions = [...allSubmissions];
                    updateStats();
                    updateTable();
                    updateCharts();
                } else {
                    console.error('Error loading data:', data.error);
                    // Fallback to localStorage
                    const storedData = localStorage.getItem('quizSubmissions');
                    allSubmissions = storedData ? JSON.parse(storedData) : [];
                    filteredSubmissions = [...allSubmissions];
                    updateStats();
                    updateTable();
                    updateCharts();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback to localStorage
                const storedData = localStorage.getItem('quizSubmissions');
                allSubmissions = storedData ? JSON.parse(storedData) : [];
                filteredSubmissions = [...allSubmissions];
                updateStats();
                updateTable();
                updateCharts();
            });'''
    )
    
    return dashboard_html

@app.route('/api/submit', methods=['POST'])
def submit_quiz():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['studentName', 'studentEmail', 'studentGrade', 'score', 
                          'totalQuestions', 'percentage', 'timeUsed', 'answers', 'incorrectAnswers']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Store in database
        conn = sqlite3.connect('quiz_results.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quiz_submissions 
            (student_name, student_email, student_grade, score, total_questions, 
             percentage, time_used, answers, incorrect_answers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['studentName'],
            data['studentEmail'],
            data['studentGrade'],
            data['score'],
            data['totalQuestions'],
            data['percentage'],
            data['timeUsed'],
            json.dumps(data['answers']),
            json.dumps(data['incorrectAnswers'])
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Quiz submitted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        conn = sqlite3.connect('quiz_results.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT student_name, student_email, student_grade, score, total_questions,
                   percentage, time_used, answers, incorrect_answers, submission_time
            FROM quiz_submissions
            ORDER BY submission_time DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                'studentName': row[0],
                'studentEmail': row[1],
                'studentGrade': row[2],
                'score': row[3],
                'totalQuestions': row[4],
                'percentage': row[5],
                'timeUsed': row[6],
                'answers': json.loads(row[7]),
                'incorrectAnswers': json.loads(row[8]),
                'submissionTime': row[9]
            })
        
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = sqlite3.connect('quiz_results.db')
        cursor = conn.cursor()
        
        # Get basic stats
        cursor.execute('SELECT COUNT(*) FROM quiz_submissions')
        total_students = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(percentage) FROM quiz_submissions')
        avg_score = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COUNT(*) FROM quiz_submissions WHERE percentage >= 80')
        excellent_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM quiz_submissions WHERE percentage < 60')
        needs_help_count = cursor.fetchone()[0]
        
        conn.close()
        
        stats = {
            'totalStudents': total_students,
            'averageScore': round(avg_score, 1),
            'excellentCount': excellent_count,
            'needsHelpCount': needs_help_count
        }
        
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
