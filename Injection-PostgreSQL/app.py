from flask import Flask, request, render_template_string
import psycopg2
import bcrypt

app = Flask(__name__)

# Koneksi ke database
def connect_db():
    try:
        return psycopg2.connect(
            dbname="injection",
            user="anggii",
            password="_Anggimaulana13",  # Gantilah dengan password yang sesuai
            host="localhost"
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Rawan SQL Injection - Register
@app.route('/vulnerable-register', methods=['GET', 'POST'])
def vulnerable_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect_db()
        if conn is None:
            return "Database connection error."

        cur = conn.cursor()

        # Rawan SQL Injection
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        try:
            cur.execute(query)
            conn.commit()
            return "Registrasi Berhasil (Rentan)!"
        except Exception as e:
            return f"Error: {e}"
        finally:
            cur.close()
            conn.close()

    return render_template_string('''
        <h2>Vulnerable Register</h2>
        <form method="POST">
            <label>Username: <input type="text" name="username" required></label><br>
            <label>Password: <input type="password" name="password" required></label><br>
            <button type="submit">Register</button>
        </form>
    ''')

# Aman dari SQL Injection - Register
@app.route('/secure-register', methods=['GET', 'POST'])
def secure_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hashing password sebelum menyimpan
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = connect_db()
        if conn is None:
            return "Database connection error."

        cur = conn.cursor()

        # Aman dari SQL Injection
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            cur.execute(query, (username, hashed_password.decode('utf-8')))
            conn.commit()
            return "Registrasi Berhasil (Aman)!"
        except Exception as e:
            return f"Error: {e}"
        finally:
            cur.close()
            conn.close()

    return render_template_string('''
        <h2>Secure Register</h2>
        <form method="POST">
            <label>Username: <input type="text" name="username" required></label><br>
            <label>Password: <input type="password" name="password" required></label><br>
            <button type="submit">Register</button>
        </form>
    ''')

# Rawan SQL Injection - Login
@app.route('/vulnerable-login', methods=['GET', 'POST'])
def vulnerable_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect_db()
        if conn is None:
            return "Database connection error."

        cur = conn.cursor()

        # Rawan SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cur.execute(query)
        user = cur.fetchone()

        if user:
            return "Login Berhasil (Rentan)!"
        return "Login Gagal!"

    return render_template_string('''
        <h2>Vulnerable Login</h2>
        <form method="POST">
            <label>Username: <input type="text" name="username" required></label><br>
            <label>Password: <input type="password" name="password" required></label><br>
            <button type="submit">Login</button>
        </form>
    ''')

# Aman dari SQL Injection - Login
@app.route('/secure-login', methods=['GET', 'POST'])
def secure_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect_db()
        if conn is None:
            return "Database connection error."

        cur = conn.cursor()

        # Aman dari SQL Injection
        query = "SELECT * FROM users WHERE username=%s"
        cur.execute(query, (username,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # user[2] adalah password hashed
            return "Login Berhasil (Aman)!"
        return "Login Gagal!"

    return render_template_string('''
        <h2>Secure Login</h2>
        <form method="POST">
            <label>Username: <input type="text" name="username" required></label><br>
            <label>Password: <input type="password" name="password" required></label><br>
            <button type="submit">Login</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
