import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import openai

# loading env variables
load_dotenv()
# OpenAI API endpoint

API_KEY = os.getenv('OPENAI_API_KEY')
API_ENDPOINT = "https://api.openai.com/v1/engines/davinci/completions"



def generate_recommendations(business_data):
    recommendations = []
    for index, row in business_data.iterrows():
        # Generate prompt for ChatGPT based on review and sentiment score
        prompt = f"Review: {row['Review']}\nSentiment Score: {row['Sentiment Score']}\nRecommendation:"
        print(f"Generating recommendation for index {index+1}...")

        # Generate completion using OpenAI API
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=50  # Adjust the number of tokens for the desired response length
        )

        if response.choices[0].finish_reason == "stop":
            completion = response.choices[0].text.strip()
            recommendations.append(completion)
        else:
            recommendations.append("Error generating recommendation")

        print(f"Recommendation generated for index {index+1}.")

        # Limit the number of recommendations to 10
        if len(recommendations) >= 10:
            break

    return recommendations[:10]


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
            recommendations = generate_recommendations(business_data)

            # Display recommendation
            for index, recommendation in enumerate(recommendations):
                st.write(f"Recommendation {index+1}:")
                st.write(recommendation)
                st.write("---")
        else:
            st.write("Error: The uploaded CSV file does not contain all the required columns.")


if __name__ == "__main__":
    openai.api_key = API_KEY
    main()
