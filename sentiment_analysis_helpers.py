from transformers import pipeline


def initialize_sentiment_analyzer():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def get_sentiment_score(sentiment_analyzer, text):
    result = sentiment_analyzer(text)
    return result[0]['score'] if result[0]['label'] == 'POSITIVE' else -result[0]['score']