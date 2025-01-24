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


REQUIRED_COLUMNS = {
    'Overall': 'Overall Sentiment',
    'Sentiment Score': 'Sentiment Score',
    'Review': 'Review Text',
    'Date': 'Date',
}


def parse_dates(date_str):
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:  
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    return None  


def validate_and_map_columns(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    missing_columns = [col for col in REQUIRED_COLUMNS.keys() if col not in df.columns]

    if missing_columns:
        Logger.warning(f"Missing columns in the data: {missing_columns}")
        st.warning("The dataset is missing some required columns. Please map the columns manually.")

        column_mapping = {
            col: st.selectbox(
                f"Select the column for '{REQUIRED_COLUMNS[col]}'",
                options=df.columns,
                key=f"column_mapping_{col}"
            )
            for col in missing_columns
        }

        for original, mapped in column_mapping.items():
            df[original] = df[mapped]
        Logger.info("Columns successfully mapped.")

    return df


def process_date_column(df: pd.DataFrame) -> pd.DataFrame:

    Logger.info("Ensuring proper parsing of the Date column with multiple formats.")
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)

    if df['Date'].isna().any():
        invalid_count = df['Date'].isna().sum()
        Logger.warning(f"{invalid_count} invalid date entries found.")
        st.warning(f"{invalid_count} rows have invalid or unrecognized date formats. These rows will be ignored.")

    return df.dropna(subset=['Date']).reset_index(drop=True)

@st.cache_data
def filter_data_by_date(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


def plot_overall_feelings(df: pd.DataFrame) -> go.Figure:
    Logger.info("Generating bar chart for overall feelings distribution.")
    counts = df['Overall'].value_counts()
    fig = go.Figure(go.Bar(x=counts.index, y=counts.values, width=0.3, marker=dict(color='purple')))
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
    fig = go.Figure(go.Violin(y=df['Sentiment Score'], box_visible=True, points="all", jitter=0.3, line_color="purple", fillcolor="purple"))
    fig.update_layout(
        title='Distribution of Sentiment Scores',
        title_x=0.35,
        yaxis_title='Sentiment Score'
    )
    return fig


def generate_graph(df: pd.DataFrame) -> go.Figure:
    Logger.info("Generating graph for overall sentiment across months.")
    df['Month'] = pd.Categorical(
        df['Date'].dt.strftime('%B'),
        categories=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        ordered=True
    )
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
        title_x=0.35,
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig


def main() -> None:
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

    df: pd.DataFrame = pd.read_csv(os.path.join(OUTPUT_PATH, selected_file))
    df = process_date_column(df)
    if df.empty:
        return

    df = validate_and_map_columns(df)
    if df is None:
        return

    # Filter data by user-selected date range
    min_date, max_date = df['Date'].min(), df['Date'].max()
    st.sidebar.subheader("Filter by Date")
    selected_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(selected_range) == 1:
        start_date = end_date = pd.to_datetime(selected_range[0])
        st.sidebar.info(f"Displaying data for {start_date.date()}")
    elif len(selected_range) == 2:
        start_date, end_date = pd.to_datetime(selected_range[0]), pd.to_datetime(selected_range[1])
        st.sidebar.info(f"Displaying data from {start_date.date()} to {end_date.date()}")
    else:
        st.sidebar.error("Invalid date range selected. Please select a valid range.")
        return

    df_filtered = filter_data_by_date(df, start_date, end_date)
    if df_filtered.empty:
        st.sidebar.warning("No data found for the selected date range.")
        return

    st.sidebar.title("Navigation")
    st.sidebar.markdown("Select any/all the Graph options below to view the data.")
    st.title('Review Data Visuals & Insights')

    selected_insights: List[str] = st.sidebar.multiselect(
        'Select Insights',
        [
            'Overall Sentiment Across Months',
            'Distribution of Overall Feelings',
            'Distribution of Sentiment Scores',
            'Sentiment Word Cloud'
        ]
    )

    if 'Distribution of Overall Feelings' in selected_insights:
        fig1 = plot_overall_feelings(df_filtered)
        st.plotly_chart(fig1)

    if 'Overall Sentiment Across Months' in selected_insights:
        fig2 = generate_graph(df_filtered)
        st.plotly_chart(fig2)

    if 'Distribution of Sentiment Scores' in selected_insights:
        fig3 = plot_sentiment_score_violin(df_filtered)
        st.plotly_chart(fig3)

    if 'Sentiment Word Cloud' in selected_insights:
        st.sidebar.subheader("Word Cloud Options")
        sentiment_choice = st.sidebar.radio(
            "Select Sentiment",
            options=["Positive", "Negative", "Neutral"]
        )
        Logger.info(f"User selected sentiment: {sentiment_choice} for word cloud.")
        fig4 = generate_word_cloud(df_filtered, sentiment_choice)
        if fig4:
            st.plotly_chart(fig4)


if __name__ == '__main__':
    main()
