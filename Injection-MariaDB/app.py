from flask import Flask, request, render_template_string
import mariadb

app = Flask(__name__)

# Database setup
DATABASE_CONFIG = {
    'user': 'root',
    'password': '_Anggimaulana13',
    'host': 'localhost',
    'database': 'secure_db',
}

def query_db(query, args=(), fetch_results=False):
    conn = mariadb.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, args)

    if fetch_results:
        result = cursor.fetchall()  # Fetch results if requested
        conn.close()
        return result

    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Rentan SQL Injection karena menggunakan string formatting langsung
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        query_db(query)
        return "User registered successfully!"

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

        # Rentan SQL Injection karena menggunakan string formatting langsung
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchall()
        conn.close()

        if user:
            return "Logged in!"
        return "Invalid credentials"

    return render_template_string("""
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    """)

@app.route('/register-aman', methods=['GET', 'POST'])
def registerAman():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Penggunaan parameterized query untuk menghindari SQL injection
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        query_db(query, (username, password))  # Tidak perlu 'fetch_results'
        return "User registered successfully!"

    return render_template_string("""
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Register</button>
        </form>
    """)

@app.route('/login-aman', methods=['GET', 'POST'])
def loginAman():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Penggunaan parameterized query untuk menghindari SQL injection
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = query_db(query, (username, password), fetch_results=True)

        if user:
            return "Logged in!"
        return "Invalid credentials"

    return render_template_string("""
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
