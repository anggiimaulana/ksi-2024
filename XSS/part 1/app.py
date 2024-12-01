from flask import Flask, request, render_template_string

app = Flask(__name__)

html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>XSS Example</title>
    </head>
    <body>
        <h1>Komentar User</h1>
        <form action="/" method="POST">
            <h1>Komentar User</h1>
            <label for="name">Nama:</label>
            <input type="text" id="name" name="name" required> <br/> <br/>
            <label for="comment">Komentar:</label>
            <textarea id="comment" name="comment" rows="4" cols="50" required></textarea>
            <button type="submit">Submit</button>
        </form>
        <div class="comment-section">
            <h2>Komentar Sebelumnya:</h2>
            {% if name and comment %}
                <div class="comment-item">
                    <strong>{{ name }}:</strong> {{ comment|safe }}
                </div>
            {% endif %}
        </div>
    </body>
    </html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    comment = None
    if request.method == "POST":
        name = request.form.get("name")
        comment = request.form.get("comment")
    
    return render_template_string(html_template, name=name, comment=comment)

if __name__ == "__main__":
    app.run(debug=True)
