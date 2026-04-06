from flask import Flask, render_template, request, flash, redirect, jsonify
import sqlite3
import json

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key="Secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])

    
    conn = get_db()

    existing_user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    

    # duplicate username validation added
    if existing_user is not None:
        conn.close()
        return render_template("register.html", message="Username already exists!")

    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return render_template("login.html", message="User registered successfully!")  

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':    
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            return render_template("dashboard.html")
        else:
            return render_template("login.html", message="Invalid credentials")
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/report_page')
def report_page():
    return render_template('report.html')

@app.route('/report', methods=['POST'])
def report():
    title = request.form['title']
    description = request.form['description']
    severity = request.form['severity']
    date = request.form['date']

    if not title or not description or not severity or not date:
        return "All fields are required"

    conn = get_db()

    conn.execute(
        "INSERT INTO incidents (title, severity, description, date) VALUES (?, ?, ?, ?)",
        (title, severity, description, date))

    conn.commit()
    conn.close()

    return render_template ("Success.html")
    
@app.route('/view')
def view():
    conn = get_db()
    incidents = conn.execute("SELECT * FROM incidents").fetchall()
    conn.close()

    return render_template("view.html", incidents=incidents)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM incidents WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/view')

@app.route('/api/incidents')
def api_incidents():
    conn = get_db()
    incidents = conn.execute("SELECT * FROM incidents").fetchall()
    conn.close()

    data = []
    for i in incidents:
        data.append({
            "id": i[0],
            "title": i[1],
            "description": i[4],
            "severity": i[3],
            "date": i[6]
        })

    return render_template("api_view.html", data=json.dumps(data, indent=4))