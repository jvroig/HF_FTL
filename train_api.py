from flask import Flask, request, jsonify
from flask_cors import CORS
from hf_local_config import *
import yaml
import openai

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

host = "3.129.14.10"
port = "8080"
model = "mixtral-8x7b-instruct-v0.1-Q3_K_M"

client = openai.OpenAI(
    base_url=f"http://{host}:{port}/v1",
    api_key = "DEBORAH-is-the-key",
    timeout=120,
)

def generate_yaml_file(data):
    # Define default values for each section
    default_config = {
        'output': {'suffix': '-FT000'},
        'dataset': {
            'type': 'json',
            'train': '',
            'eval': '',
            'use_hf_datasets': False,
            'hf_dataset_name': '',
            'hf_splits': []
        },
        'model': {
            'path': '',
            'name': '',
            'type': 'causallm',
            'class': ''
        },
        'tokenizer': {
            'class': '',
            'add_pad_token': False,
            'pad_token': 'eos_token',
            'padding_side': 'right'
        },
        'from_pretrained': {
            'torch_dtype': ''
        },
        'lora': {
            'use_lora': False,
            'r': 8,
            'alpha': 32,
            'dropout': 0.05,
            'target_modules': ['q', 'v', 'k', 'o', 'wi_0', 'wi_1', 'wo'],
            'bias': 'none',
            'task_type': 'CAUSAL_LM'
        },
        'quant': {
            'quantize': False,
            'load_in_4bit': True,
            'bnb_4bit_quant_type': 'nf4',
            'bnb_4bit_use_double_quant': True,
            'bnb_4bit_compute_dtype': 'bf16'
        },
        'train_args': {
            'num_epochs': 1,
            'load_best_model_at_end': False,
            'per_device_train_batch_size': 1,
            'per_device_eval_batch_size': 1,
            'gradient_accumulation_steps': 1,
            'warmup_steps': 100,
            'save_steps': 5000,
            'weight_decay': 0.1,
            'learning_rate': 0.0005,
            'logging_steps': 10,
            'gradient_checkpointing': True,
            'optim': 'adafactor',
            'evaluation_strategy': 'epoch',
            'save_strategy': 'steps',
            'logging_strategy': 'epoch',
            'log_level': 'warning'
        }
    }


    # Update default values with data from the frontend if available
    for key, value in data.items():
        if key in default_config:
            default_config[key].update(value)

    # Construct the YAML file name based on ft_name
    suffix = data.get('output', 'default_name').get('suffix', 'default_name')
    yaml_filename = f"train_{suffix}.yaml"

    # Write the YAML file
    with open(yaml_filename, 'w') as yaml_file:
        yaml.dump(default_config, yaml_file)

    return yaml_filename

@app.route('/api/train', methods=['POST'])
def start_training():
    data = request.get_json()
    if data:
        yaml_file = generate_yaml_file(data)
        response_message = f"YAML file '{yaml_file}' created successfully."
    else:
        response_message = "Error: No data received from frontend."

    response = {"message": response_message}
    return jsonify(response)

@app.route('/api/config', methods=['GET'])
def get_config_paths():
    config_paths = {
        "model_path": model_path,
        "finetuned_path": finetuned_path
    }
    return jsonify(config_paths)

@app.route('/api/query_endpoint', methods=['POST'])
def query_endpoint():
    payload = request.get_json()
    # print(payload)
    # return jsonify(payload)
    prompt = payload['prompt']
    temperature = payload['temperature']
    max_output_tokens = payload['max_output_tokens']

    # messages = [
    #     {"role": "user", "content": f"[INST]{prompt}[/INST]"}
    # ]
    messages = [
        {"role": "user", "content": prompt}
    ]

    # print(messages)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=int(max_output_tokens),
    )

    return {'message': response.choices[0].message.content}


if __name__ == '__main__':
    app.run(debug=True, port="5001")

