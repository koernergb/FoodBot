from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json
from utils import print_pantries, generate_user_context
from datetime import datetime
from transformers import AutoTokenizer




app = Flask(__name__)



# Load the food pantry data from the JSON file
with open('C:/Users/16168/Documents/SideProjects/food_bot/src/food_pantries.json', 'r') as file:
    food_pantries = json.load(file)


print_pantries(food_pantries, 42, 83)
instruct_str = f"""You are tasked with helping users looking for food distribution resources in their area.
    You have access to the user's query and a context for that user.
    This user context lists the food pantries in the database along with their phone number, address, and relevant notes.
    It also includes a list of the distances from the user to the food pantries in the database. 
    Finally, it includes a list of the upcoming open distribution sessions for these pantries for the next 10 days. 
    Use your general knowledge and the given user context to concisely answer the user query, 
    which may include questions about the nearest food pantries and when they are next open"""
context = generate_user_context(42, 83, datetime.now(), food_pantries)
context = context + instruct_str
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased") 
tokens = tokenizer.tokenize(context)

print(f"Number of tokens: {len(tokens)}")

# Load the GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)


@app.route('/')
def home():
    string = context
    return string 

# API endpoint for processing user queries
@app.route('/query', methods=['POST'])
def process_query():
    data = request.get_json()
    user_query = data['query']

    # Generate a response using the model
    input_ids = tokenizer.encode(user_query, return_tensors='pt')
    output = model.generate(input_ids, max_length=150, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)