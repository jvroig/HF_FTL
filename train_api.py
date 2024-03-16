from flask import Flask, request, jsonify
from flask_cors import CORS
from hf_local_config import *
import ast

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

@app.route('/api/message', methods=['POST'])
def receive_message():
    data = request.get_json()

    # Construct the response message
    response_message = "Received the following data:\n"
    for key, value in data.items():
        response_message += f"{key}: {value}\n"

    response = {"message": response_message}
    return jsonify(response)

@app.route('/api/config', methods=['GET'])
def get_config_paths():
    config_paths = {
        "model_path": model_path,
        "finetuned_path": finetuned_path
    }
    return jsonify(config_paths)

@app.route('/api/get_data', methods=['GET'])
def get_data():
    filename = request.args.get('filename')  # Get filename from query parameter
    filename = 'sample.logs' #Debugging line only
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            data = []
            for line in lines:
                try:
                    entry = ast.literal_eval(line.strip())  # Parse Python dict string to dict
                    if 'loss' in entry or 'eval_loss' in entry:
                        data.append(entry)
                except SyntaxError:
                    pass  # Ignore lines that are not valid Python dictionary strings
            return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port="5001")

