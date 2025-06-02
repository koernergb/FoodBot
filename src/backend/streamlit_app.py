import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set the URL of your Flask app's API endpoint
API_URL = "http://localhost:5000/query"

def main():
    st.title("Food Pantry Chatbot")

    # Get user input
    user_query = st.text_input("Enter your query:")

    # Get user's location
    logger.debug("Attempting to get geolocation data...")
    geolocation_data = streamlit_geolocation()
    logger.debug(f"Geolocation data received: {geolocation_data}")

    if geolocation_data:
        user_latitude = geolocation_data['latitude']
        user_longitude = geolocation_data['longitude']

        st.write("Latitude:", user_latitude)
        st.write("Longitude:", user_longitude)

        if st.button("Send"):
            logger.debug(f"Sending request with query: {user_query}")
            logger.debug(f"Location: lat={user_latitude}, lon={user_longitude}")
            
            try:
                # Make a POST request to the Flask app's API endpoint
                payload = {
                    "query": user_query,
                    "latitude": user_latitude,
                    "longitude": user_longitude
                }
                logger.debug(f"Request payload: {payload}")
                
                response = requests.post(API_URL, json=payload)
                logger.debug(f"Response status code: {response.status_code}")
                logger.debug(f"Response content: {response.content}")

                if response.status_code == 200:
                    # Display the chatbot's response
                    chatbot_response = response.json()["response"]
                    st.write("Chatbot:", chatbot_response)
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    st.write(f"Error occurred while processing the query. {error_msg}")
            except requests.exceptions.ConnectionError:
                error_msg = f"Could not connect to Flask backend at {API_URL}. Is the Flask server running?"
                logger.error(error_msg)
                st.error(error_msg)
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                logger.error(error_msg)
                st.error(error_msg)
    else:
        st.write("Geolocation data not available.")
        logger.warning("No geolocation data available")

if __name__ == "__main__":
    main()