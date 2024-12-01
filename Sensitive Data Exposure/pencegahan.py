from flask import Flask, render_template, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Koneksi ke database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'injeksion',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

def get_mahasiswa_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as err:
        print(f"Error: {err}")
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def api_data():
    api_key = request.headers.get('X-API-Key')
    if api_key != 'my_api_key':
        return jsonify({"error": "Data tidak ditemukan"}), 401
    
    data = get_mahasiswa_data()
    if not data:
        return jsonify({"error": "Data tidak ditemukan"}), 404
    return jsonify({"data": data})

    
if __name__ == '__main__':
    app.run(debug=True)