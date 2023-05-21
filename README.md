# Multilingual Sentiment Analysis Tool For Your Business

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/yourusername/yourrepository/blob/main/LICENSE)

## Overview

The Multilingual Sentiment Analysis Tool is a powerful solution designed to help businesses gain valuable insights into customer sentiments across multiple languages. By analyzing review scores and providing actionable recommendations using OpenAI GPT models, this tool empowers local businesses to make data-driven decisions and enhance customer satisfaction.

Business Recommendation Example
![image](https://github.com/john-thuo1/Multilingual_SentimentAnalysis_Tool/assets/108690517/ebe17922-a5bb-4665-8478-26b333859aea)

## Key Features

- Multilingual sentiment analysis: Supports languages such as English, Dutch, French, and more, with plans to expand to diverse African languages like Kiswahili.
- Comprehensive insights: Analyzes review scores and generates informative graphs including line graphs, box plots...
- Actionable recommendations: Provides businesses with tailored recommendations for improving customer experiences and overall performance.
- Powered by state-of-the-art models: Utilizes Hugging Face's ***'nlptown/bert-base-multilingual-uncased-sentiment'*** model for accurate sentiment analysis.
- User-friendly interface: Offers an intuitive and easy-to-use interface for businesses to access and interpret analysis results.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
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

1. Prepare your review data in a suitable format (Must have Date, Review, Month, Year columns).

2. Upload the Data on the application.

3. Download the Updated Dataset. It should be populated with new Sentiment Score & Overall Columns.

4. To check the various Data Graphs, check 'insights' on the side-menu and upload the Updated Dataset.

5. On the insights, an option to choose the type of graph will be displayed. You can view 1 or all graphs.

6. After, head to Business Recommendation and Upload the Updated Reviews Dataset. 

3. The tool will analyze the review scores and generate informative graphs to visualize the sentiment insights.

4. Review the analysis results( and recommendations provided by the tool. 
    - The program will automatically generate the Recommendation using OpenAI's Engine ***text-davinci-003***,

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request. For major changes, please discuss them first in the issue tracker.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## Acknowledgments

- The Multilingual Sentiment Analysis Tool was built using the ***nlptown/bert-base-multilingual-uncased-sentiment*** model from Hugging Face.

## Contact

For any inquiries or feedback, please contact [john](mailto:j.mwangi@alustudent.com).

## Next Steps

- Expand language support to include diverse African languages like Kiswahili.
- Enhance the sentiment analysis model to handle nuanced sentiments and improve accuracy.
- Incorporate real-time data analysis capabilities for monitoring customer sentiments.
- Develop advanced recommendation algorithms based on sentiment analysis for tailored strategies.

---

By leveraging advanced sentiment analysis techniques and powerful visualizations, the Multilingual Sentiment Analysis Tool equips businesses with the insights needed to thrive in diverse linguistic landscapes.
