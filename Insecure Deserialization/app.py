import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Deserialization</h1>
    <form action="/deserialize" method="POST">
        <label for="data">Serialized Data (JSON):</label><br />
        <textarea id="data" name="data" rows="4" cols="50"></textarea> <br/> <br/>
        <input type="submit" value="Submit">
    </form>
    """

@app.route('/deserialize', methods=['POST'])
def deserialize():
    try:
        serialized_data = request.form['data']
        
        # Batasi input hanya pada JSON yang valid
        if not serialized_data:
            return jsonify({"error": "No data provided"}), 400
        
        # Lakukan validasi pada input sebelum deserialisasi
        if not isinstance(serialized_data, str):
            return jsonify({"error": "Input must be a JSON string"}), 400
        
        # Deserialisasi JSON
        deserialized_object = json.loads(serialized_data)

        # Tambahkan validasi pada data hasil deserialisasi (jika diperlukan)
        if not isinstance(deserialized_object, dict):
            return jsonify({"error": "Deserialized object must be a JSON object"}), 400

        return jsonify({
            "message": "Data deserialized successfully",
            "deserialized_object": deserialized_object
        })
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
