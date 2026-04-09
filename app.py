from flask import Flask, render_template, request, flash, redirect, jsonify, session
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        severity TEXT,
        date TEXT,
        user TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

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
    password = request.form['password']

    if not username or not password:
        return "All fields required"

    hashed_password = generate_password_hash(password)

    conn = get_db()

    existing_user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if existing_user:
        conn.close()
        return render_template("register.html", message="Username already exists")

    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )

    conn.commit()
    conn.close()

    return render_template("login.html", message="Registered successfully") 

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
            session['user'] = username
            return redirect('/dashboard')
        else:
          flash("Invalid username or password")
          return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    
    return render_template("dashboard.html")

@app.route('/report_page')
def report_page():
        return render_template('report.html')

@app.route('/report', methods=['POST'])
def report():
    if 'user' not in session:
        return redirect('/')

    title = request.form['title']
    description = request.form['description']
    severity = request.form['severity']
    date = request.form['date']
    user = session['user']
   
    if not title or not description or not severity or not date:
        return "All fields are required"

    conn = get_db()

    conn.execute(
        "INSERT INTO incidents (title, description, severity, date, user) VALUES (?, ?, ?, ?, ?)",
        (title, description, severity, date, user))

    conn.commit()
    conn.close()

    return render_template ("Success.html")

    
@app.route('/view')
def view():
    if 'user' not in session:
        return redirect('/')

    user = session['user']  

    conn = get_db()
    incidents = conn.execute(
        "SELECT * FROM incidents WHERE user = ?",
        (user,)
    ).fetchall()
    conn.close()

    return render_template("view.html", incidents=incidents)

@app.route('/delete/<int:id>')
def delete(id):

    if 'user' not in session:
        return redirect('/') 

    user = session['user']

    conn = get_db()
    conn.execute(
        "DELETE FROM incidents WHERE id = ? AND user = ?",
        (id, user)
    )
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


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')