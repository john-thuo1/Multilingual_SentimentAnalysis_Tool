import os
from typing import List, Optional
import streamlit as st
import pandas as pd
from openai import OpenAI
# from decouple import config

from Home import OUTPUT_PATH
from src.utils import setup_logger
from streamlit_chat import message

# Setup logger
Logger = setup_logger(logger_file="app")


def truncate_text(text, max_length):
    return text[:max_length] + "..." if len(text) > max_length else text


def generate_initial_recommendation(client, business_data):
    message = ""
    for _, row in business_data.iterrows():
        review = truncate_text(row['Review'], 500)
        sentiment_score = row['Sentiment Score']
        message += f"Review: {review}\nSentiment Score: {sentiment_score}\n"
    message = truncate_text(message, 4096)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Provide a thorough Business Recommendation based on the reviews and sentiment scores."},
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message.content.strip()


def generate_follow_up_response(client, chat_history):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )
    return response.choices[0].message.content.strip()


def main():
    st.title("Business Recommendation Chat")
    st.markdown(
    """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        This section allows you to use updated customer review data with the sentiment scores 
        to generate insightful business recommendations using OpenAI's GPT-4 Model 🚀 !!!
    """,
    unsafe_allow_html=True)

    # Ask for the OpenAI API key
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    if not api_key:
        st.warning("Please enter your OpenAI API key to proceed.")
        st.stop()

    # Instantiate the OpenAI client
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        Logger.error(f"Failed to initialize OpenAI client: {e}")
        st.error("Invalid API key. Please try again.")
        st.stop()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_selected_file" not in st.session_state:
        st.session_state.last_selected_file = None
    if "initial_recommendation_done" not in st.session_state:
        st.session_state.initial_recommendation_done = False

    csv_files: List[str] = [f for f in os.listdir(OUTPUT_PATH) if f.endswith('.csv')]

    if not csv_files:
        Logger.warning(f"No CSV files found in the directory: {OUTPUT_PATH}")
        st.error(f"No CSV files found in the directory: {OUTPUT_PATH}")
        return

    selected_file: Optional[str] = st.sidebar.selectbox("Select the File to analyze", csv_files)

    if not selected_file:
        Logger.warning("No file selected by the user.")
        st.error("No file selected.")
        return

    # Detect file change
    if st.session_state.last_selected_file != selected_file:
        st.session_state.last_selected_file = selected_file
        st.session_state.initial_recommendation_done = False  
        st.session_state.chat_history = []  
    Logger.info(f"File selected: {selected_file}")

    try:
        df: pd.DataFrame = pd.read_csv(
            os.path.join(OUTPUT_PATH, selected_file),
            parse_dates=['Date'],
            infer_datetime_format=True
        )
        Logger.info(f"File {selected_file} loaded successfully.")
    except Exception as e:
        Logger.error(f"Error loading file {selected_file}: {e}")
        st.error(f"Error loading file: {str(e)}")
        return

    if df.empty:
        Logger.warning(f"The file {selected_file} contains no data.")
        st.error("The selected file contains no data.")
        return

    required_columns = ["Review", "Sentiment Score"]
    if set(required_columns).issubset(df.columns):
        if not st.session_state.initial_recommendation_done:
            recommendation = generate_initial_recommendation(client, df)
            st.session_state.chat_history.append({"role": "assistant", "content": recommendation})
            st.session_state.initial_recommendation_done = True

        for chat_message in st.session_state.chat_history:
            if chat_message["role"] == "user":
                message(chat_message['content'], is_user=True)
            else:
                message(chat_message['content'], is_user=False)
        prompt = st.chat_input("Follow Up Question? Inquire from here ...")
        if prompt:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            follow_up_response = generate_follow_up_response(client, st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": follow_up_response})
            st.rerun()
    else:
        st.error("Error: The uploaded CSV file does not contain all the required columns.")

if __name__ == "__main__":
    main()
