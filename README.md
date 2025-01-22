# Multilingual Sentiment Analysis Tool For Your Business

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/yourusername/yourrepository/blob/main/LICENSE)

## Overview

The Multilingual Sentiment Analysis Tool is a powerful solution designed to help businesses gain valuable insights into customer sentiments across multiple languages. By analyzing review scores and providing actionable recommendations using OpenAI GPT models, this tool empowers local businesses to make data-driven decisions and enhance customer satisfaction.

## HomePage
![image](https://github.com/user-attachments/assets/b4c45c92-e702-4368-b4e2-fad0b93bf1b0)
![image](https://github.com/user-attachments/assets/3bf13e67-bf32-4d68-9739-f5bb28a98c13)

## Data Visuals 
![image](https://github.com/user-attachments/assets/5a5159a5-9c27-4537-a808-6f331e49e865)

## Recommendations
![image](https://github.com/user-attachments/assets/828baa7b-102a-4425-ad1b-37d441ba2744)



## Key Features
- Powered by models such as Hugging Face's ***'nlptown/bert-base-multilingual-uncased-sentiment'*** model for accurate sentiment analysis and ***gpt4o model*** for recommendations.
- Comprehensive insights - Analyzes review scores and generates informative graphs including 
- Actionable recommendations - Provides businesses with tailored recommendations for improving customer experiences and overall performance.
- Powered by state-of-the-art models - Utilizes Hugging Face's ***'nlptown/bert-base-multilingual-uncased-sentiment'*** model for accurate sentiment analysis.
- User-friendly interface - Offers an intuitive and easy-to-use interface for businesses to access and interpret analysis results.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/john-thuo1/Multilingual_SentimentAnalysis_Tool
   cd into your directory/ open with vscode
   ```
2. Create a Virtual Environment:
    ```shell
    python -m venv env
    ```
3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```
4. Create OpenAI API Key and add it to your .env file:
   [openai](https://platform.openai.com/)
   
5. Run the application:

   ```shell
   streamlit run sentiment.py
   ```

## Usage

1. Prepare your review data in a suitable format(have Date, Review, Month, and Year columns). You can also match the required columns when uploading the file.

2. The application will download the updated dataset and store it within. You can also download it from the browser. It should be populated with new Sentiment Score & Overall Columns.

3. To check the various Data Graphs, check 'Data Visuals'. These graphs will use the updated data.

4. Still on the Visuals, an option to choose the type of graph will be displayed. You can view 1 or all graphs.

7. Lastly, head to 'Recommendations' for Business Insights informed by your Data and OpenAI's ***gpt4o model***.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request. For major changes, please discuss them first in the issue tracker.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## Acknowledgments

- The Multilingual Sentiment Analysis Tool was built using the ***nlptown/bert-base-multilingual-uncased-sentiment*** model from Hugging Face.

## Next Steps

- Expand language support to include diverse African languages like Kiswahili.
- Enhance the sentiment analysis model to handle nuanced sentiments and improve accuracy.
- Incorporate real-time data analysis capabilities for monitoring customer sentiments.
- Implement Session Management across multiple pages to improve UI.

---
