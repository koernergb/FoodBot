from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2

from flask import render_template



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Load the pre-trained model and tokenizer
model_name = "gpt2"  # Replace with the desired model name
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Load the food pantry data (assuming it's in the format mentioned earlier)
food_pantries = [
    # ... (food pantry data here)
]

# Helper functions (list_next_openings, calculate_distance, generate_prompt_data)
def list_next_openings(current_date):
    # ... (implementation remains the same)
    pass

def calculate_distance(lat1, lon1, lat2, lon2):
    # ... (implementation remains the same)
    pass

def generate_prompt_data(user_latitude, user_longitude):
    # ... (implementation remains the same)
    pass

# API endpoint for processing user queries
@app.route('/query', methods=['POST'])
def process_query():
    data = request.get_json()
    user_query = data['query']
    user_latitude = data['latitude']
    user_longitude = data['longitude']

    prompt_data = generate_prompt_data(user_latitude, user_longitude)

    # Combine the user query with the prompt data
    full_prompt = f"User query: {user_query}\n\n{prompt_data}\n\nAssistant:"

    # Generate a response using the model
    input_ids = tokenizer.encode(full_prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=150, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)