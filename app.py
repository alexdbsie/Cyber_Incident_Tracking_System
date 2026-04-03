from flask import Flask, render_template, request, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

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
    if existing_user:
        conn.close()
    return render_template("success.html", message="Username already exists!")

    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return render_template("success.html", message="Registration successful!")  

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db()
    user = conn.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user[0], password):
        return render_template("success.html", message="Login successful!")
    else:
        return render_template("success.html", message="Invalid credentials!")