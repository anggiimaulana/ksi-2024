from flask import Flask, request, render_template_string
import cx_Oracle

app = Flask(__name__)

# Menyambung ke Oracle Database
def get_db_connection():
    try:
        dsn = cx_Oracle.makedsn('localhost', '1521', 'XE') 
        connection = cx_Oracle.connect('system', 'anggi1307', dsn)
        return connection
    except cx_Oracle.Error as e:
        return None 

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
        <p>Belum punya akun? <a href="/register">Daftar disini</a></p>
    ''')

# Halaman Form Register
@app.route("/register", methods=["GET"])
def register_form():
    return render_template_string('''
        <h1>Register</h1>
        <form action="/register" method="POST">
            <label>Username: <input type="text" name="username" /></label><br />
            <label>Password: <input type="password" name="password" /></label><br />
            <button type="submit">Daftar</button>
        </form>
        <p>Sudah punya akun? <a href="/">Login disini</a></p>
    ''')

# Endpoint Login
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Menyambung ke database
    connection = get_db_connection()
    
    if connection is None:
        return "Gagal terhubung ke database. Pastikan konfigurasi koneksi benar."
    
    cursor = connection.cursor()

    try:
        # Query untuk memeriksa username dan password - Rentan terhadap SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return f"Login berhasil! Selamat datang, {result[1]}"  # Misalnya nama pengguna ada di kolom kedua
        else:
            return "Login gagal, username atau password salah."
    except cx_Oracle.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        connection.close()

# Endpoint Register
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Menyambung ke database
    connection = get_db_connection()
    
    if connection is None:
        return "Gagal terhubung ke database. Pastikan konfigurasi koneksi benar."
    
    cursor = connection.cursor()

    try:
        # Query untuk memeriksa apakah username sudah ada - Rentan terhadap SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username sudah digunakan, silakan coba username lain."
        
        # Query untuk menambahkan pengguna baru - Rentan terhadap SQL Injection
        insert_query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        cursor.execute(insert_query)
        connection.commit()  # Pastikan perubahan disimpan ke database
        
        return "Pendaftaran berhasil! Silakan login."
    except cx_Oracle.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        connection.close()

# Jalankan server Flask
if __name__ == "__main__":
    app.run(debug=True, port=5000)
