import tkinter as tk
from tkinter import messagebox
import pyodbc
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Konfigurasi koneksi ke SQL Server
def connect_to_database():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=UNKNOW;'  # Ganti sesuai nama server SQL Server Anda
            'DATABASE=injeksion;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"Koneksi ke database gagal: {e}")
        return None

# Inisialisasi koneksi database
connection = connect_to_database()
if connection:
    cursor = connection.cursor()

# Halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validasi apakah username sudah ada (Aman dari SQL Injection)
        query_check = "SELECT * FROM Users WHERE username = ?"
        cursor.execute(query_check, (username,))
        result = cursor.fetchone()

        if result:
            return "Username sudah digunakan! Coba yang lain.", 400

        # Menambahkan user baru ke database (Aman dari SQL Injection)
        query_insert = "INSERT INTO Users (username, password) VALUES (?, ?)"
        cursor.execute(query_insert, (username, password))
        connection.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Login dengan query parameterized (Aman dari SQL Injection)
        query = "SELECT * FROM Users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            return f"Selamat datang, {username}!"
        else:
            return "Username atau password salah!", 401

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
