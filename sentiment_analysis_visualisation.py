import matplotlib.pyplot as plt
import seaborn as sns


def plot_monthly_sentiment(monthly_sentiment):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=monthly_sentiment, x='month', y='sentiment_score')
    plt.title('Monthly Sentiment Trends in NYT Articles (2022)')
    plt.xlabel('Month')
    plt.ylabel('Average Sentiment Score')
    plt.show()

def plot_sentiment_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='sentiment_score', bins=2)
    plt.title('Distribution of Article Sentiments')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Count')
    plt.show()