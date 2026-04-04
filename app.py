from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
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

    existing_user = conn.execute("SELECT * FROM users WHERE username = ?", 
                    (username,)).fetchone()
    

    # duplicate username validation added
    if existing_user is not None:
        conn.close()
        return render_template("register.html", message="Username already exists!")

    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   (username, password))
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

    conn = get_db()

    conn.execute(
        "INSERT INTO incidents (title, description, severity, date) VALUES (?, ?, ?, ?)",
        (title, description, severity, date)
    )

    conn.commit()
    conn.close()

    return render_template ("Success.html")
    
@app.route('/view')
def view():
    conn = get_db()
    incidents = conn.execute("SELECT * FROM incidents").fetchall()
    conn.close()

    return render_template("view.html", incidents=incidents)