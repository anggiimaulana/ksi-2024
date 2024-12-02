from flask import Flask, request, render_template_string, session, redirect, url_for
import mysql.connector
from bcrypt import hashpw, gensalt, checkpw
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Secure Secret Key
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-dev-key')

# Database configuration from environment variables
DATABASE = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Database helper function with parameterized queries
def query_db(query, args=(), one=False):
    conn = mysql.connector.connect(**DATABASE)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, args)
    result = cursor.fetchone() if one else cursor.fetchall()
    conn.commit()
    conn.close()
    return result

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)
        if existing_user:
            return "Username already exists. Please choose a different one."

        # Hash the password
        hashed_password = hashpw(password.encode('utf-8'), gensalt())

        # Insert user with parameterized query
        query_db("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        return redirect(url_for('login'))
    return render_template_string("""
        <form method="post">
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <button type="submit">Register</button>
        </form>
    """)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from database
        user = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)

        # Check if user exists and password matches
        if user and checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['username'] = username
            return "Logged in successfully!"
        return "Invalid username or password."

    return render_template_string("""
        <form method="post">
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <button type="submit">Login</button>
        </form>
    """)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Use environment variable to toggle debug mode
    app.run(debug=os.getenv('FLASK_ENV') == 'development')
