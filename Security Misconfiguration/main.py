from flask import Flask, request, render_template_string, session
import mysql.connector

app = Flask(__name__)

# Misconfiguration: Hardcoded Secret Key
app.secret_key = 'hardcoded-secret-key'  # Tidak aman, seharusnya gunakan variabel lingkungan.

# Database setup
DATABASE = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'injeksion',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Misconfiguration: Input tanpa sanitasi (SQL Injection risk)
def query_db(query, args=(), one=False):
    conn = mysql.connector.connect(**DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    conn.close()
    return (result[0] if result else None) if one else result

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connector.connect(**DATABASE)
        cursor = conn.cursor()
        try:
            # Celah: Data langsung dimasukkan tanpa hashing
            cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")  
            conn.commit()
            return "User registered!"
        except Exception as e:
            return f"Registration failed: {e}"
        finally:
            conn.close()
    return render_template_string("""
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Register</button>
        </form>
    """)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connector.connect(**DATABASE)
        cursor = conn.cursor()
        try:
            # Celah: SQL Injection
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")  
            user = cursor.fetchone()
            if user:
                session['username'] = username
                return "Logged in!"
            else:
                return "Invalid credentials"
        except Exception as e:
            return f"Login failed: {e}"
        finally:
            conn.close()
    return render_template_string("""
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    """)

if __name__ == '__main__':
    app.run(debug=True)  # DEBUG mode aktif (misconfiguration)
