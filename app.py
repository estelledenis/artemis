import sqlite3
from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Artemis Station"


# Challenge 1 - Docking Bay Crew Search - Vulnerable to SQL Injection
@app.route('/docking')
def docking():
    return render_template('docking.html')

@app.route('/search' , methods=['POST'])
def search():
    if request.method == 'POST':
        crew_name = request.form['crew_members']

        # Intentionally vulnerable to SQL Injection for CTF purposes
        query = f"SELECT * FROM crew_members WHERE name LIKE '%{crew_name}%'"

        # Connect to SQLite database and execute the query
        connection = sqlite3.connect('artemis.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        connection.close()

        # Render results
        return render_template('search_results.html', results=results, query=query)
    
@app.route('/verify_access', methods=['POST'])
def verify_access():
    access_code = request.form['access_code']

    if access_code == 'ARTEMIS{DOCK-ACCESS-7734}':
        return render_template('docking_success.html')
    else:
        return render_template('docking.html', error='Invalid access code.')


# Challenge 2 - Life Support System Log Submission - Vulnerable to XSS
@app.route('/life_support')
def life_support():
    return render_template('life_support.html')

@app.route('/submit_log', methods=['POST'])
def submit_log():
    user_name = request.form['user_name']
    log_entry = request.form['log_entry']

    # Connect to SQLite database and insert the log entry
    connection = sqlite3.connect('artemis.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO maintenance_logs (user_name, log_entry, status)
        VALUES (?, ?, 'pending')
    ''', (user_name, log_entry))
    connection.commit()
    connection.close()

    return render_template('life_support.html', success='Log entry submitted successfully.')
    
@app.route('/view_logs')
def view_logs():
    # Connect to SQLite database and retrieve all maintenance logs
    connection = sqlite3.connect('artemis.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM maintenance_logs ORDER BY timestamp DESC')
    logs = cursor.fetchall()
    connection.close()

    return render_template('view_logs.html', logs=logs)

@app.route('/admin_panel')
def admin_panel():
    connection = sqlite3.connect('artemis.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM maintenance_logs WHERE status = "pending" ORDER BY timestamp DESC')
    logs = cursor.fetchall()
    connection.close()

    response = make_response(render_template('admin_panel.html', logs=logs))
    response.set_cookie('admin_token', 'ARTEMIS{LIFE-SUPPORT-OMEGA}')
    return response

@app.route('/verify_life_support', methods=['POST'])
def verify_life_support():
    token = request.form['access_code']
    if token == 'ARTEMIS{LIFE-SUPPORT-OMEGA}':
        return render_template('life_support_success.html')
    else:
        return render_template('life_support.html', error='Invalid token.')

if __name__ == '__main__':
    app.run(debug=True)