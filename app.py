from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production
CORS(app)

# Teacher credentials (in production, use a proper database)
TEACHER_CREDENTIALS = {
    'admin': hashlib.sha256('password123'.encode()).hexdigest()  # Change this password
}

# Database setup
def init_db():
    try:
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
                quiz_type TEXT DEFAULT 'database',
                submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e

# Initialize database on startup
init_db()

# Login required decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'teacher_logged_in' not in session:
            return redirect(url_for('teacher_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CAT Quiz System</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
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
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
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
            .btn-excel {
                background: linear-gradient(135deg, #fd7e14, #e55a00);
            }
            .btn-excel:hover {
                box-shadow: 0 5px 15px rgba(253, 126, 20, 0.3);
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
            .teacher-link {
                text-align: center;
                margin-top: 30px;
            }
            .teacher-link a {
                color: rgba(255,255,255,0.7);
                text-decoration: none;
                font-size: 0.9em;
                transition: color 0.3s;
            }
            .teacher-link a:hover {
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 CAT Quiz System</h1>
                <p>Grade 11 CAT - Database & Excel Learning Platform</p>
            </div>
            
            <div class="cards">
                <div class="card">
                    <h3>🗄️ Database Quiz</h3>
                    <p>Complete the 25-question pre-assessment quiz to evaluate your Microsoft Access database knowledge. 30-minute timed assessment with immediate feedback.</p>
                    <a href="/quiz" class="btn">Start Database Quiz</a>
                </div>
                
                <div class="card">
                    <h3>📈 Excel Quiz</h3>
                    <p>Test your Excel skills with the Marks Analysis quiz. Practice functions like SUM, AVERAGE, IF, COUNTIF, and more with instant feedback.</p>
                    <a href="/excel-quiz" class="btn btn-excel">Start Excel Quiz</a>
                </div>
                
                <div class="card">
                    <h3>📚 Study Notes</h3>
                    <p>Access comprehensive, interactive notes covering all Microsoft Access database concepts. Perfect for self-study and revision.</p>
                    <a href="/notes" class="btn btn-notes">View Database Notes</a>
                </div>
                
                <div class="card">
                    <h3>📊 Excel Notes</h3>
                    <p>Comprehensive Excel study guide covering functions, formulas, and practical examples. Perfect for Excel quiz preparation.</p>
                    <a href="/excel-notes" class="btn btn-excel">View Excel Notes</a>
                </div>
            </div>

            <div class="features">
                <h2>🎯 Features</h2>
                <div class="features-grid">
                    <div class="feature">
                        <div class="feature-icon">⏱️</div>
                        <h3>Timed Assessment</h3>
                        <p>30-minute database quiz with real-time progress tracking</p>
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
                        <h3>Excel Practice</h3>
                        <p>Auto-graded Excel quiz with instant feedback</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">📈</div>
                        <h3>Performance Analytics</h3>
                        <p>Detailed student performance tracking and analysis</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">🌐</div>
                        <h3>Online Access</h3>
                        <p>Accessible from anywhere with internet connection</p>
                    </div>
                </div>
            </div>
            
            <div class="teacher-link">
                <a href="/teacher-login">👨‍🏫 Teacher Access</a>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/teacher-login')
def teacher_login():
    if 'teacher_logged_in' in session:
        return redirect(url_for('teacher_dashboard'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teacher Login - CAT Quiz System</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 400px;
                text-align: center;
            }
            .login-container h1 {
                color: #2c3e50;
                margin-bottom: 30px;
                font-size: 2em;
            }
            .form-group {
                margin-bottom: 20px;
                text-align: left;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #495057;
                font-weight: 500;
            }
            .form-group input {
                width: 100%;
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 16px;
                box-sizing: border-box;
            }
            .form-group input:focus {
                outline: none;
                border-color: #007bff;
            }
            .btn {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
            }
            .back-link {
                margin-top: 20px;
            }
            .back-link a {
                color: #6c757d;
                text-decoration: none;
            }
            .back-link a:hover {
                color: #007bff;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>👨‍🏫 Teacher Login</h1>
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            <form method="POST" action="/teacher-login">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
            <div class="back-link">
                <a href="/">← Back to Student Portal</a>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/teacher-login', methods=['POST'])
def teacher_login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in TEACHER_CREDENTIALS and TEACHER_CREDENTIALS[username] == hashlib.sha256(password.encode()).hexdigest():
        session['teacher_logged_in'] = True
        session['teacher_username'] = username
        return redirect(url_for('teacher_dashboard'))
    else:
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Teacher Login - CAT Quiz System</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .login-container {
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    width: 100%;
                    max-width: 400px;
                    text-align: center;
                }
                .login-container h1 {
                    color: #2c3e50;
                    margin-bottom: 30px;
                    font-size: 2em;
                }
                .form-group {
                    margin-bottom: 20px;
                    text-align: left;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 8px;
                    color: #495057;
                    font-weight: 500;
                }
                .form-group input {
                    width: 100%;
                    padding: 12px;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    font-size: 16px;
                    box-sizing: border-box;
                }
                .form-group input:focus {
                    outline: none;
                    border-color: #007bff;
                }
                .btn {
                    width: 100%;
                    padding: 15px;
                    background: linear-gradient(135deg, #007bff, #0056b3);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.3s;
                }
                .btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
                }
                .back-link {
                    margin-top: 20px;
                }
                .back-link a {
                    color: #6c757d;
                    text-decoration: none;
                }
                .back-link a:hover {
                    color: #007bff;
                }
                .error {
                    background: #f8d7da;
                    color: #721c24;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h1>👨‍🏫 Teacher Login</h1>
                <div class="error">Invalid username or password. Please try again.</div>
                <form method="POST" action="/teacher-login">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn">Login</button>
                </form>
                <div class="back-link">
                    <a href="/">← Back to Student Portal</a>
                </div>
            </div>
        </body>
        </html>
        ''')

@app.route('/teacher-logout')
def teacher_logout():
    session.pop('teacher_logged_in', None)
    session.pop('teacher_username', None)
    return redirect(url_for('index'))

@app.route('/teacher-dashboard')
@login_required
def teacher_dashboard():
    # Serve the dashboard HTML file
    try:
        with open('CAT_Grade11_Database_Dashboard.html', 'r', encoding='utf-8') as f:
            dashboard_html = f.read()
        return dashboard_html
    except FileNotFoundError:
        return "Dashboard file not found. Please check if CAT_Grade11_Database_Dashboard.html exists.", 404
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/quiz')
def quiz():
    try:
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
    except FileNotFoundError:
        return "Quiz file not found. Please check if CAT_Grade11_Database_Quiz_25Questions_Enhanced.html exists.", 404
    except Exception as e:
        return f"Error loading quiz: {str(e)}", 500

@app.route('/excel-quiz')
def excel_quiz():
    # Serve the enhanced Excel quiz HTML file
    try:
        with open('CAT_Excel_Marks_Analysis_Quiz_Enhanced.html', 'r', encoding='utf-8') as f:
            excel_quiz_html = f.read()
    except FileNotFoundError:
        return "Excel quiz file not found. Please check if CAT_Excel_Marks_Analysis_Quiz_Enhanced.html exists.", 404
    except Exception as e:
        return f"Error loading excel quiz: {str(e)}", 500
    
    # Replace the localStorage submission with API call
    excel_quiz_html = excel_quiz_html.replace(
        'function submitToBackend(quizData) {',
        '''function submitToBackend(quizData) {
            // Submit to Railway backend API
            fetch('/api/submit-excel', {
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
    
    return excel_quiz_html

@app.route('/notes')
def notes():
    # Serve the enhanced notes HTML file
    try:
        with open('CAT_Database_Enhanced_Notes.html', 'r', encoding='utf-8') as f:
            notes_html = f.read()
    except FileNotFoundError:
        return "Database notes file not found. Please check if CAT_Database_Enhanced_Notes.html exists.", 404
    except Exception as e:
        return f"Error loading database notes: {str(e)}", 500
    return notes_html

@app.route('/excel-notes')
def excel_notes():
    # Serve the Excel study notes HTML file
    try:
        with open('CAT_Excel_Study_Notes.html', 'r', encoding='utf-8') as f:
            excel_notes_html = f.read()
    except FileNotFoundError:
        return "Excel notes file not found. Please check if CAT_Excel_Study_Notes.html exists.", 404
    except Exception as e:
        return f"Error loading excel notes: {str(e)}", 500
    return excel_notes_html

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
             percentage, time_used, answers, incorrect_answers, quiz_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['studentName'],
            data['studentEmail'],
            data['studentGrade'],
            data['score'],
            data['totalQuestions'],
            data['percentage'],
            data['timeUsed'],
            json.dumps(data['answers']),
            json.dumps(data['incorrectAnswers']),
            'database'
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Quiz submitted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/submit-excel', methods=['POST'])
def submit_excel_quiz():
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
             percentage, time_used, answers, incorrect_answers, quiz_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['studentName'],
            data['studentEmail'],
            data['studentGrade'],
            data['score'],
            data['totalQuestions'],
            data['percentage'],
            data['timeUsed'],
            json.dumps(data['answers']),
            json.dumps(data['incorrectAnswers']),
            'excel'
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
                   percentage, time_used, answers, incorrect_answers, quiz_type, submission_time
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
                'quiz_type': row[9],
                'submissionTime': row[10]
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

@app.route('/api/debug', methods=['GET'])
def debug_database():
    """Debug route to check database contents"""
    try:
        conn = sqlite3.connect('quiz_results.db')
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_submissions'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            return jsonify({
                'success': False, 
                'error': 'Table does not exist',
                'message': 'The quiz_submissions table has not been created yet.'
            })
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM quiz_submissions')
        total_count = cursor.fetchone()[0]
        
        # Get sample data
        cursor.execute('SELECT * FROM quiz_submissions LIMIT 3')
        sample_data = cursor.fetchall()
        
        # Get quiz type distribution
        cursor.execute('SELECT quiz_type, COUNT(*) FROM quiz_submissions GROUP BY quiz_type')
        quiz_types = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'success': True,
            'table_exists': table_exists,
            'total_submissions': total_count,
            'sample_data': sample_data,
            'quiz_type_distribution': quiz_types,
            'message': f'Database contains {total_count} submissions'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test')
def test():
    """Simple test route to verify the application is working"""
    return jsonify({
        'success': True,
        'message': 'CAT Quiz System is running correctly!',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'main_page': '/',
            'teacher_login': '/teacher-login',
            'teacher_dashboard': '/teacher-dashboard',
            'database_quiz': '/quiz',
            'excel_quiz': '/excel-quiz',
            'database_notes': '/notes',
            'excel_notes': '/excel-notes',
            'api_results': '/api/results',
            'api_debug': '/api/debug'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
