from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# Koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="injeksion",
    charset="utf8mb4",
    collation="utf8mb4_general_ci"
)

# Halaman Form Login
@app.route("/", methods=["GET"])
def login_form():
    return render_template_string('''
        <h1>Login</h1>
        <form action="/login" method="POST">
            <label>Username: <input type="text" name="username" /></label><br />
            <label>Password: <input type="password" name="password" /></label><br />
            <button type="submit">Login</button>
        </form>
    ''')

# Endpoint Login
@app.route("/login", methods=["POST"])
def login():
    # Mengambil data username dan password dari form
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Query SQL
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    cursor = db.cursor(dictionary=True)
    try:
        # Menjalankan query dengan parameter
        cursor.execute(query)
        results = cursor.fetchall()

        # Memeriksa apakah hasil query mengembalikan data
        if len(results) > 0:
            return f"Login berhasil! Selamat datang, {results[0]['username']}"
        else:
            return "Login gagal, username atau password salah."
    except mysql.connector.Error as err:
        # Menangani error database
        return f"Error: {err}"
    finally:
        cursor.close() # Selalu tutup cursor setelah selesai

# Jalankan server Flask
if __name__ == "__main__":
    app.run(debug=True, port=5000)
