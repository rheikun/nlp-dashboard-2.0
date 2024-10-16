# Sentiment Analysis Application

This application utilizes Natural Language Processing (NLP) techniques to analyze and predict the sentiment of comments from users. Users can input text to receive instant predictions on whether the sentiment of the comment is positive, negative, or neutral.

## Key Features

- **Sentiment Analysis**: 
  Enter any sentence or words, and the application will classify its sentiment using a trained Naive Bayes model. Users will receive a prediction along with a corresponding emoji that represents the sentiment.

- **Analysis Overview**: 
  The application provides visual insights into the comments bbased on the dataset utilized by the author, including:
  - **Word Clouds**: Visual representations of the most frequently used words in comments categorized by sentiment. Larger words indicate higher frequency.
  - **Bar Charts**: Graphical displays of the top words used in positive, negative, and neutral comments, helping users understand the common themes and sentiments expressed.
  - **Most Common Words**: A table displaying the most frequently used words across all comments, giving an overview of the main topics discussed.

## Dataset Source

The dataset used in this application is derived from YouTube comments related to presidential and vice-presidential debates, allowing for a focused analysis of public opinion.

## Disclaimer

Please note that the sentiment analysis results may not fully capture the nuances of user opinions. The model leverages NLP techniques, which may have limitations in understanding context and linguistic subtleties.

## Preview Interface

If you're curious about how the app works, you can check the link in [url.txt](rheikun/nlp-dashboard-2.0/blob/main/url.txt) and access it from your browser.

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_yt_nlp
cd proyek_yt_nlp
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run streamlit app
```
streamlit run dashboard.py
```
