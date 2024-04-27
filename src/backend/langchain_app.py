from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import json
from utils import generate_user_context
import cohere
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Load the Cohere API key from the environment variables
load_dotenv()
api_key = os.environ["COHERE_API_KEY"]

# Initialize the Cohere client and LLM
co = cohere.Client(api_key)
llm = Cohere(cohere_api_key=api_key)

# Load the food pantry data from the JSON file
json_path = "C:/Users/16168/Documents/SideProjects/food_bot/src/food_pantries.json"
with open(json_path, 'r') as file:
    food_pantries = json.load(file)

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["user_query", "prompt_context"],
    template="""You are tasked with helping users looking for food distribution resources in their area. You have access to the user's query and a context providing information about local food pantries.

    User query: {user_query}
    User context:
    {prompt_context}
    Your Response:
    """
)

# Create an LLMChain using the Cohere LLM and the prompt template
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

# API endpoint for processing user queries
@app.route('/query', methods=['POST'])
def process_query():
    data = request.get_json()
    user_query = data['query']
    user_latitude = data['latitude']
    user_longitude = data['longitude']
    current_time = datetime.now()
    prompt_context = generate_user_context(user_latitude, user_longitude, current_time, food_pantries)

    # Generate a response using the LLMChain
    response = llm_chain.run(user_query=user_query, prompt_context=prompt_context)

    return jsonify({'response': response})

@app.route('/')
def home():
    context = generate_user_context(42, 83, datetime.now(), food_pantries)
    example_query = "What's the next open food pantry?"

    # Generate a response using the LLMChain
    response = llm_chain.run(user_query=example_query, prompt_context=context)

    string = f"User Query:\n{example_query}\nUser Context:\n{context}\nResponse:\n{response}"
    return string

if __name__ == '__main__':
    app.run(debug=True)