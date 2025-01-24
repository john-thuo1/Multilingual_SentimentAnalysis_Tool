# Multilingual Sentiment Analysis Tool For Your Business Reviews

[Deployed Application](https://multilingualsentimentanalysistool.streamlit.app/)

## Overview

The **Multilingual Sentiment Analysis Tool** helps businesses gain valuable insights into customer sentiments by analyzing review scores. Powered by OpenAI GPT models, this tool provides actionable recommendations, empowering local businesses to make data-driven decisions and enhance customer satisfaction.

## HomePage
![image](https://github.com/user-attachments/assets/b4c45c92-e702-4368-b4e2-fad0b93bf1b0)
![image](https://github.com/user-attachments/assets/3bf13e67-bf32-4d68-9739-f5bb28a98c13)

## Data Visuals 
![image](https://github.com/user-attachments/assets/5a5159a5-9c27-4537-a808-6f331e49e865)

## Recommendations
![image](https://github.com/user-attachments/assets/b1380c6a-33fb-4f38-b044-2596bc014c7a)
![image](https://github.com/user-attachments/assets/9da9c564-d615-4518-b3e1-7acc5f1a2348)

## Key Features
- **Multilingual Sentiment Analysis**: Powered by Hugging Face's `nlptown/bert-base-multilingual-uncased-sentiment` model for accurate sentiment analysis in multiple languages.
- **Actionable Business Insights**: The tool generates tailored recommendations using OpenAI's GPT-4 model, helping businesses improve customer experiences.
- **Comprehensive Data Visualization**: Analyzes review scores and generates various insightful graphs.
- **User-Friendly Interface**: Intuitive and easy-to-use, allowing businesses to quickly interpret the analysis results.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/john-thuo1/Multilingual_SentimentAnalysis_Tool
   cd into your directory/ open with vscode
   ```

2. Create a virtual environment:

   ```shell
   python -m venv env
   ```

3. Install the required dependencies:

   ```shell
   uv pip install -r requirements.txt
   ```

4. Create an OpenAI API Key and Enter it on the Input Field in the Recommendations Page to proceed:
   [openai](https://platform.openai.com/)

5. Run the application:

   ```shell
   streamlit run Home.py
   ```

## Usage

1. Prepare your review data in a suitable format, with at least `Date`, `Review`, `Month`, and `Year` columns. (You can use different column names, but ensure the application can match them during analysis.)
   
2. The application will download the updated dataset and store it locally. You can also download it directly from the browser, and it will include new columns for Sentiment Scores and Overall Sentiment.

3. For viewing various data graphs, navigate to the 'Data Visuals' section. You can explore different types of graphs based on the updated data.

4. In the 'Visuals' section, choose the type of graph you want to display. You can select one or all available graphs.

5. Finally, go to the 'Recommendations' section for tailored business insights powered by the OpenAI GPT-4 model. Enter the OpenAI API Key before proceeding to get insights.

## Contributing

Contributions are welcome! If you have ideas, suggestions, or bug reports, feel free to open an issue or submit a pull request. For major changes, please discuss them first in the issue tracker.

## Acknowledgments

- The **Multilingual Sentiment Analysis Tool** is built using Hugging Face's `nlptown/bert-base-multilingual-uncased-sentiment` model for sentiment analysis.
- OpenAI GPT models provide actionable recommendations for businesses.

## Next Steps

- Expand language support to include diverse African languages, such as Kiswahili.
- Modify the data input requirement to only need the `Date` field for analysis instead of `Date`, `Month`, and `Year`.
- Enhance the sentiment analysis model to handle nuanced sentiments and improve accuracy.
- Incorporate real-time data analysis capabilities for continuous monitoring of customer sentiment.
