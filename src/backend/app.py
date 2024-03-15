from flask import Flask, request, jsonify
from transformers import LlamaForCausalLM, LlamaTokenizer
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import json
from utils import generate_user_context

app = Flask(__name__)

# Load the LLAMA 2 model and tokenizer
model_name = "openlm-research/open_llama_7b"
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name)

# Load the food pantry data from the JSON file
json_path = "C:/Users/16168/Documents/SideProjects/food_bot/src/food_pantries.json"
with open(json_path, 'r') as file:
    food_pantries = json.load(file)

# API endpoint for processing user queries
@app.route('/query', methods=['POST'])


def process_query():
    data = request.get_json()
    user_query = data['query']
    user_latitude = data['latitude']
    user_longitude = data['longitude']

    current_time = datetime.now()
    prompt_context = generate_user_context(user_latitude, user_longitude, current_time, food_pantries)

    # Construct the full prompt
    instruction_prompt = f"""You are tasked with helping users looking for food distribution resources in their area.
    You have access to the user's query and a context for that user.
    This user context lists the food pantries in the database along with their phone number, address, and relevant notes.
    It also includes a list of the distances from the user to the food pantries in the database. 
    Finally, it includes a list of the upcoming open distribution sessions for these pantries for the next 10 days. 
    Use your general knowledge and the given user context to concisely answer the user query, 
    which may include questions about the nearest food pantries and when they are next open"""
    query_and_context = f"User query: {user_query}\nUser context:\n{prompt_context}\nYour Response:\n"
    full_prompt = instruction_prompt + query_and_context
    
    # Generate a response using the model
    input_ids = tokenizer.encode(full_prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=4096, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return jsonify({'response': response})

@app.route('/')
def home():
    context = generate_user_context(42, 83, datetime.now(), food_pantries)
    example_query = "What's the nearest food pantry?"
    instruction_prompt = f"""You are tasked with helping users looking for food distribution resources in their area.
    You have access to the user's query and a context for that user.
    This user context lists the food pantries in the database along with their phone number, address, and relevant notes.
    It also includes a list of the distances from the user to the food pantries in the database. 
    Finally, it includes a list of the upcoming open distribution sessions for these pantries for the next 10 days. 
    Use your general knowledge and the given user context to concisely answer the user query, 
    which may include questions about the nearest food pantries and when they are next open"""
    prompt = instruction_prompt + "\n User Query: \n " + example_query + "\n User Context: \n" + context
    
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=4096, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    string = prompt + "\n" + response
    return string 


if __name__ == '__main__':
    app.run(debug=True)