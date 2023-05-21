# Business Recommendation Page
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import openai

# Loading env variables
load_dotenv()

def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def generate_recommendation(business_data, api_key):
    # Generate prompt for ChatGPT based on reviews and sentiment scores
    prompt = ""
    for index, row in business_data.iterrows():
        review = row['Review']
        sentiment_score = row['Sentiment Score']
        # Truncate the review if it exceeds a certain length
        review = truncate_text(review, 500)
        prompt += f"Review: {review}\nSentiment Score: {sentiment_score}\n"

    # Truncate prompt to a maximum length of 4096 tokens
    prompt = truncate_text(prompt, 4096)

    # Generate completion using OpenAI API
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt + "\nProvide a recommendation for the business based on the uploaded data:",
        max_tokens=100,  # Increased the max_tokens value for a longer response
    )

    if response.choices[0].finish_reason == "stop":
        recommendation = response.choices[0].text.strip()
    else:
        recommendation = "Error generating recommendation"

    return recommendation


def main():
    st.title("Business Recommendation")

    # Upload CSV file
    file = st.file_uploader("Upload a CSV file", type=["csv"])

    if file is not None:
        business_data = pd.read_csv(file)

        # Display uploaded data
        st.subheader("Uploaded Business Data")
        st.write(business_data)

        # Check if required columns exist
        required_columns = ["Review", "Sentiment Score", "Date", "Month", "Year"]
        if set(required_columns).issubset(business_data.columns):
            st.subheader("Business Recommendation")
            api_key = os.getenv('OPENAI_API_KEY')
            recommendation = generate_recommendation(business_data, api_key)

            # Display recommendation
            st.write("Summary Recommendation:")
            st.write(str(recommendation))  # Convert recommendation to string
        else:
            st.write("Error: The uploaded CSV file does not contain all the required columns.")


if __name__ == "__main__":
    main()
