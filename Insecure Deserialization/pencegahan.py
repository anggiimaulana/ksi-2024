from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Deserialization with Flask</h1>
    <form id="jsonForm">
        <label for="data">Serialized Data (JSON):</label><br />
        <textarea id="data" name="data" rows="4" cols="50"></textarea><br/><br/>
        <input type="submit" value="Submit">
    </form>

    <script>
        document.getElementById('jsonForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const data = document.getElementById('data').value;

            fetch('/deserialize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ data: data })
            })
            .then(response => response.json())
            .then(responseData => {
                alert('Response: ' + JSON.stringify(responseData));
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    </script>
    """

@app.route('/deserialize', methods=['POST'])
def deserialize():
    try:
        # Ambil data JSON dari body request
        data = request.get_json()

        # Validasi apakah data ada
        if not data or 'data' not in data:
            return jsonify({"error": "No data provided"}), 400

        serialized_data = data['data']

        # Validasi apakah data adalah JSON yang valid
        deserialized_object = json.loads(serialized_data)

        # Validasi lebih lanjut pada struktur objek JSON
        if not isinstance(deserialized_object, dict):  # Misalnya, hanya mengizinkan objek JSON
            return jsonify({"error": "Deserialized object must be a JSON object"}), 400

        # Kembalikan hanya pesan tanpa mengembalikan deserialized object
        return jsonify({
            "message": "Data deserialized successfully"
        })

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
