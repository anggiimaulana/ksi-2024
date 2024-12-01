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
    nama = request.args.get('nama')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        if nama:
            cursor.execute("SELECT * FROM users WHERE username LIKE %s", (f"%{nama}%",))
        else:
            cursor.execute("SELECT * FROM users")
        
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        return jsonify({"data" :data})
    except Error as err:
        print(f"Error: {err}")
        return jsonify({"error": "Internal server error"}), 500 
    
if __name__ == '__main__':
    app.run(debug=True)