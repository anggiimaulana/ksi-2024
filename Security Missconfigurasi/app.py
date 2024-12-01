from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Selamat datang! <br> Klik <a href='/config'>di sini</a> untuk melihat konfigurasi."

@app.route('/config')
def config():
    # Konfigurasi rentan, menampilkan detail sensitif
    return str(app.config)

if __name__ == '__main__':
    app.run(debug=True)
