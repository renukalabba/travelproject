import streamlit as st
import os
import google.generativeai as genai

# API Key
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"

# Function to get API key
def get_api_key():
    secret_key = None
    try:
        secret_key = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        secret_key = None
    return secret_key or os.getenv("GOOGLE_API_KEY") or GOOGLE_API_KEY


# Build Gemini Model with generation configuration
def build_model():

    generation_config = {
        "temperature": 0.4,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config
    )

    return model


# Function to generate itinerary
def generate_itinerary(model, destination, days, nights):

    prompt = f"""
    Write a detailed travel itinerary for a trip to {destination}
    for {days} days and {nights} nights.

    Include:
    - Daily schedule
    - Famous tourist attractions
    - Food recommendations
    - Travel tips
    """

    response = model.generate_content(prompt)

    return response.text


# Main Streamlit App
def main():

    st.title("Travel Itinerary Generator")
    st.write("Generate your travel plan using AI ✈️")

    api_key = get_api_key()

    if not api_key:
        st.error("Google API key not found.")
        st.stop()

    # Activity 2.2: Configure Gemini API
    genai.configure(api_key=api_key)

    try:
        # Activity 2.3: Initialize Gemini model
        model = build_model()
        st.caption("Using model: gemini-1.5-flash")

    except Exception as e:
        st.error(f"Failed to initialize Gemini model: {e}")
        st.stop()

    # User Inputs
    destination = st.text_input("Enter your desired destination:")

    days = st.number_input("Enter the number of days:", min_value=1)

    nights = st.number_input("Enter the number of nights:", min_value=0)

    # Generate Button
    if st.button("Generate Itinerary"):

        if destination.strip() and days > 0 and nights >= 0:

            try:
                with st.spinner("Generating your itinerary..."):
                    itinerary = generate_itinerary(model, destination, days, nights)

                st.text_area(
                    "Generated Itinerary:",
                    value=itinerary,
                    height=300
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

        else:
            st.error("Please make sure all inputs are provided and valid.")


# Run App
if __name__ == "__main__":
    main()