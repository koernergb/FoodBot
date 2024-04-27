import streamlit as st
from streamlit_geolocation import streamlit_geolocation

import requests

# Set the URL of your Flask app's API endpoint
API_URL = "http://localhost:5000/query"

def main():
    st.title("Food Pantry Chatbot")

    # Get user input
    user_query = st.text_input("Enter your query:")

    # Get user's location
    geolocation_data = streamlit_geolocation()

    if geolocation_data:
        user_latitude = geolocation_data['latitude']
        user_longitude = geolocation_data['longitude']

        st.write("Latitude:", user_latitude)
        st.write("Longitude:", user_longitude)

        if st.button("Send"):
            # Make a POST request to the Flask app's API endpoint
            response = requests.post(API_URL, json={
                "query": user_query,
                "latitude": user_latitude,
                "longitude": user_longitude
            })

            if response.status_code == 200:
                # Display the chatbot's response
                chatbot_response = response.json()["response"]
                st.write("Chatbot:", chatbot_response)
            else:
                st.write("Error occurred while processing the query.")
    else:
        st.write("Geolocation data not available.")

if __name__ == "__main__":
    main()