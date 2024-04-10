import googleapiclient.discovery
import pandas as pd
import creds
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

def fetch_youtube_comments(video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=creds.DEVELOPER_KEY)
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100, # Maximum allowed by Youtube Data API
            pageToken=next_page_token if next_page_token else ""
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])

def preprocess_comment(comment):
    # Lowercase everything
    comment = comment.lower()
    # Remove URL's
    comment = re.sub(r"http\S+", "", comment)
    # Remove special characters
    comment = re.sub(r"[^a-zA-Z\s]", "", comment)
    # Remove extra whitespace
    comment = re.sub(r"\s+", " ", comment)
    
    # Tokenize comment
    tokens = word_tokenize(comment)
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return ' '.join(tokens)

def analyze_sentiment(comments):
    cleaned_comments = [preprocess_comment(comment) for comment in comments]
    df = pd.DataFrame(cleaned_comments, columns=['text'])
    analyzer = SentimentIntensityAnalyzer()

    sentiment_scores = []

    for comment_token in df["text"]:
        sentiment = analyzer.polarity_scores(comment_token)
        sentiment_scores.append(sentiment)

    return sentiment_scores

def visualize_sentiment(sentiment_scores):
    compound_score = [score["compound"] for score in sentiment_scores]

    plt.figure(figsize=(8,6))
    plt.hist(compound_score, bins=20, color="orange", edgecolor="black", label="With Neutral")
    plt.title("Distribution of Compound Sentiment Scores With Neutral Results")
    plt.xlabel('Compound Sentiment Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def main():
    video_id = "uJMCNJP2ipI"
    comments_df = fetch_youtube_comments(video_id)
    sentiment_scores = analyze_sentiment(comments_df["text"])
    visualize_sentiment(sentiment_scores)

if __name__ == "__main__":
    main()
