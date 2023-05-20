import base64
import streamlit as st
import pandas as pd
import seaborn as sns

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import matplotlib.pyplot as plt

# Load the NLP Model from Hugging Face
def load_model():
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    return tokenizer, model

# Sentiment Scoring
def sentiment_score(review, tokenizer, model):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits) + 1)

def generate_sentiment_boxplot(df):
    # Create the box plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(df.groupby('Month')['Sentiment Score'].apply(list).values)
    ax.set_title('Sentiment Scores by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Sentiment Score')

    # Set x-axis tick labels
    ax.set_xticks(range(1, len(df['Month'].unique()) + 1))
    ax.set_xticklabels(df['Month'].unique())

    return fig

def main():
    st.title("Multilingual Sentiment Analysis Tool For Your Business")
    csv_file = st.file_uploader("Please upload Your Business' Reviews", type=["csv"])

    if csv_file is not None:
        df = pd.read_csv(csv_file)
        df['Sentiment Score'] = 0  # Add the 'Sentiment Score' column with default values
        snapshot = df.head(3)
        st.dataframe(snapshot)  # Display the first 3 rows

        # Load the model
        tokenizer, model = load_model()

        # Press this button to see results
        if st.button("Analyze"):
            # Perform sentiment analysis on the 'Review' column
            df['Sentiment Score'] = df['Review'].apply(lambda x: sentiment_score(x, tokenizer, model))

            # Display the updated DataFrame
            st.dataframe(df.head())

            csv_file_name = 'updated_reviews.csv'
            csv = df.to_csv(index=False)

            st.download_button(
                label='Download CSV File',
                data=csv,
                file_name=csv_file_name,
                mime='text/csv'
            )

        # Option to generate graphs
        if st.button("Generate Graphs"):
            # Ensure the 'Sentiment Score' column is present
            if 'Sentiment Score' not in df.columns:
                st.write("Please analyze the reviews first to generate sentiment scores.")
            else:
                # Generate and display graphs here
                fig = generate_sentiment_boxplot(df)
                st.pyplot(fig)

if __name__ == '__main__':
    main()
