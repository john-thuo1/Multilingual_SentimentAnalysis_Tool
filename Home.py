import os
import streamlit as st
import pandas as pd
import datetime
from omegaconf import OmegaConf
import typing as tp
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from src.utils import setup_logger

# Set up logger
Logger = setup_logger(logger_file="app")

# Load configuration
config = OmegaConf.load('./config.yml')
OUTPUT_PATH = config.general.OUTPUT_DATA_FOLDER


# Load the NLP Model from Hugging Face
@st.cache_data 
def load_model() -> tp.Tuple[AutoTokenizer, AutoModelForSequenceClassification]:
    try:
        Logger.info("Loading model and tokenizer from Hugging Face...")
        tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        Logger.info("Model and tokenizer loaded successfully.")
        return tokenizer, model
    except (ImportError, FileNotFoundError, IOError) as e:
        Logger.error(f"Error loading model: {e}")


# Sentiment Scoring
def sentiment_score(review: str, tokenizer: AutoTokenizer, model: AutoModelForSequenceClassification) -> int:
    tokens = tokenizer.encode(str(review), return_tensors='pt', truncation=True, padding=True, max_length=512)
    result = model(tokens).logits  
    sentiment = int(torch.argmax(result) + 1)
    return sentiment
    

def format_review(option: str) -> str:
    return f"⭐ {option}"


def is_review_column(column: pd.Series) -> bool:
    return column.apply(lambda x: isinstance(x, str) and len(x.split()) > 3).sum() > 0


def convert_to_csv(df: pd.DataFrame) -> bytes:
    try:
        Logger.info("Converting DataFrame to CSV...")
        return df.to_csv().encode('utf-8')
    except (ValueError, TypeError, IndexError, FileNotFoundError, KeyError) as e:
        Logger.error(f"Error converting DataFrame to CSV: {e}")


def main() -> None:
    st.title("Opinion Mining Tool For Your Business")
    csv_file = st.file_uploader("Please upload Your Business' Reviews", type=["csv"])

    if csv_file is not None:
        Logger.info(f"CSV file uploaded: {csv_file.name}")
        df = pd.read_csv(csv_file)

        # Prompt the user to select a column for reviews
        selected_column = st.selectbox(
            label="Please select the column that contains the reviews",
            options=df.columns.tolist(),
            format_func=format_review
        )

        if selected_column:
            Logger.info(f"User selected column: {selected_column}")
            df['Review'] = df[selected_column].astype(str)

            if not is_review_column(df[selected_column]):
                st.warning(f"The selected column '{selected_column}' doesn't seem to contain valid reviews. Please reselect!")
                Logger.warning(f"The selected column '{selected_column}' does not contain valid reviews.")

            snapshot = df[[selected_column]].head(3)
            st.dataframe(snapshot, width=800)

            tokenizer, model = load_model()

            if st.button("Analyze"):
                Logger.info("Sentiment analysis started...")
                df['Sentiment Score'] = df['Review'].apply(
                    lambda x: sentiment_score(x[:512], tokenizer, model) if pd.notna(x) else 0
                )

                sentiment_mapping = {5: 'Positive', 4: 'Positive', 3: 'Neutral', 1: 'Negative', 2: 'Negative'}
                df['Overall'] = df['Sentiment Score'].map(sentiment_mapping)

                st.dataframe(df.head())

                file_name = csv_file.name.split('.')[0]
                csv_file_name = f"{file_name}_updated_reviews_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"
                csv_file_path = os.path.join(OUTPUT_PATH, csv_file_name)

                if os.path.exists(csv_file_path):
                    Logger.info(f"File already exists at: {csv_file_path}. Skipping file saving.")
                    st.warning(f"The file '{csv_file_name}' already exists. It will not be overwritten.")
                else:
                    df.to_csv(csv_file_path, index=False, encoding="utf-8")
                    Logger.info(f"File saved successfully at: {csv_file_path}")
                    st.success(f"File has been saved successfully at: {csv_file_path}")


                # Provide download button for the user
                with open(csv_file_path, "rb") as input_file:
                    st.download_button(
                        label="Download CSV File From Browser?",
                        data=input_file,
                        file_name=csv_file_name,
                        mime="text/csv"
                    )


if __name__ == '__main__':
    main()
