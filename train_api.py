from flask import Flask, request, jsonify
from flask_cors import CORS
from hf_local_config import *

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

@app.route('/api/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    message = data['message']
    response = {"message": f"I received your message. Your message was: {message}"}
    return jsonify(response)

@app.route('/api/config', methods=['GET'])
def get_config_paths():
    config_paths = {
        "model_path": model_path,
        "finetuned_path": finetuned_path
    }
    return jsonify(config_paths)

if __name__ == '__main__':
    app.run(debug=True)

