import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import os
from typing import List, Optional
from Home import OUTPUT_PATH
from wordcloud import WordCloud
from src.utils import setup_logger

# Setup logger
Logger = setup_logger(logger_file="app")

# Required columns for the application
REQUIRED_COLUMNS = {
    'Overall': 'Overall Sentiment',
    'Sentiment Score': 'Sentiment Score',
    'Review': 'Review Text',
    'Month': 'Month',
    'Date': 'Date',
}


# Column validation and mapping function
def validate_and_map_columns(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    missing_columns = [col for col in REQUIRED_COLUMNS.keys() if col not in df.columns]

    if missing_columns:
        Logger.warning(f"Missing columns in the data: {missing_columns}")
        st.warning("The dataset is missing some required columns. Please map the columns manually.")

        # Display a column mapping interface
        column_mapping = {}
        for col in missing_columns:
            column_mapping[col] = st.selectbox(
                f"Select the column for '{REQUIRED_COLUMNS[col]}'",
                options=df.columns,
                key=f"column_mapping_{col}"
            )

        # Update the DataFrame with the mapped columns
        try:
            for original, mapped in column_mapping.items():
                df[original] = df[mapped]
            Logger.info("Columns successfully mapped.")
        except Exception as e:
            Logger.error(f"Error mapping columns: {e}")
            st.error("Error mapping columns. Please ensure the selected columns are correct.")
            return None

    return df

# Bar Chart: Distribution of Overall Feelings
def plot_overall_feelings(df: pd.DataFrame) -> go.Figure:
    Logger.info("Generating bar chart for overall feelings distribution.")
    counts = df['Overall'].value_counts()
    fig = go.Figure(go.Bar(x=counts.index, y=counts.values, width=0.3))
    fig.update_layout(
        title='Distribution of Overall Feelings',
        title_x=0.35,
        xaxis_title='Overall Feeling',
        yaxis_title='Count',
        xaxis={'categoryorder': 'total descending'},
        bargap=0.1,
    )
    return fig

def plot_sentiment_score_violin(df: pd.DataFrame) -> go.Figure:
    Logger.info("Generating violin plot for sentiment score distribution.")
    fig = go.Figure(go.Violin(y=df['Sentiment Score'], box_visible=True, points="all", jitter=0.3, fillcolor="purple"))
    fig.update_layout(
        title='Distribution of Sentiment Scores',
        title_x=0.35,
        yaxis_title='Sentiment Score'
    )
    return fig

# Sentiment across different months with ordered months (January to December)
def generate_graph(df: pd.DataFrame) -> go.Figure:
    Logger.info("Generating graph for overall sentiment across months.")
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    # Ensure the 'Month' column is ordered correctly
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    sentiment_counts = df.groupby(['Month', 'Overall']).size().reset_index(name='Count')

    fig = go.Figure()
    for label in sentiment_counts['Overall'].unique():
        df_filtered = sentiment_counts[sentiment_counts['Overall'] == label]
        fig.add_trace(go.Scatter(
            x=df_filtered['Month'],
            y=df_filtered['Count'],
            mode='lines+markers',
            name=label
        ))

    fig.update_layout(
        title='Overall Sentiment Across Months',
        title_x=0.35,
        xaxis_title='Month',
        yaxis_title='Count of Scores',
        legend_title='Sentiment'
    )
    return fig

def generate_word_cloud(df: pd.DataFrame, sentiment: str) -> go.Figure:
    Logger.info(f"Generating word cloud for sentiment: {sentiment}")
    try:
        filtered_reviews = df[df['Overall'] == sentiment]['Review'].dropna()
        text = " ".join(filtered_reviews)

        wordcloud = WordCloud(
            width=800, height=400, background_color="white", colormap="viridis"
        ).generate(text)

        fig = go.Figure()
        fig.add_layout_image(
            dict(
                source=wordcloud.to_image(),
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                xanchor="left",
                yanchor="top",
                layer="below"
            )
        )
        fig.update_layout(
            title=f"Word Cloud for {sentiment} Sentiments",
            xaxis={"visible": False},
            yaxis={"visible": False},
            margin=dict(l=0, r=0, t=50, b=0)
        )
        return fig
    except Exception as e:
        Logger.error(f"Error generating word cloud for {sentiment}: {e}")
        st.error(f"Could not generate the word cloud for {sentiment}. Please check the data.")
        return None

def main() -> None:
    try:
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

        Logger.info(f"File selected: {selected_file}")
        try:
            df: pd.DataFrame = pd.read_csv(
                os.path.join(OUTPUT_PATH, selected_file),
                parse_dates=['Date'])
            Logger.info(f"File {selected_file} loaded successfully.")
        except Exception as e:
            Logger.error(f"Error loading file {selected_file}: {e}")
            st.error(f"Error loading file: {str(e)}")
            return

        if df.empty:
            Logger.warning(f"The file {selected_file} contains no data.")
            st.error("The selected file contains no data.")
            return

        # Validate and map columns
        df = validate_and_map_columns(df)
        if df is None:
            return

        st.sidebar.title("Navigation")
        st.sidebar.markdown("Use the options below to explore the data.")
        st.title('Review Data Visuals & Insights')
        st.sidebar.title('Filter Options')

        selected_insights: List[str] = st.sidebar.multiselect(
            'Select Insights',
            [
                'Overall Sentiment Across Months',
                'Distribution of Overall Feelings',
                'Distribution of Sentiment Scores',
                'Sentiment Word Cloud',
            ]
        )

        if 'Distribution of Overall Feelings' in selected_insights:
            fig1 = plot_overall_feelings(df)
            st.plotly_chart(fig1)

        if 'Overall Sentiment Across Months' in selected_insights:
            fig2 = generate_graph(df)
            st.plotly_chart(fig2)

        if 'Distribution of Sentiment Scores' in selected_insights:
            fig3 = plot_sentiment_score_violin(df)
            st.plotly_chart(fig3)

        if 'Sentiment Word Cloud' in selected_insights:
            st.sidebar.subheader("Word Cloud Options")
            sentiment_choice = st.sidebar.radio(
                "Select Sentiment",
                options=["Positive", "Negative", "Neutral"]
            )
            Logger.info(f"User selected sentiment: {sentiment_choice} for word cloud.")
            fig4 = generate_word_cloud(df, sentiment_choice)
            if fig4:
                st.plotly_chart(fig4)

    except Exception as e:
        Logger.error(f"Unexpected error: {e}")
        st.error("An unexpected error occurred. Please check the logs.")

if __name__ == '__main__':
    main()
