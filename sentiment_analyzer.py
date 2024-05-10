import googleapiclient.discovery
import pandas as pd
import creds
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    #Extract the video ID from a full YouTube URL.
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    video_id = query.get("v")
    if video_id:
        return video_id[0]
    else:
        # Handle shortened YouTube URLs
        pattern = r"(youtu\.be/|youtube.com/(embed/|v/|shorts/))([^\?&\"' >]+)"
        match = re.search(pattern, url)
        return match.group(3) if match else None
    
def fetch_youtube_comments(url_or_id):
    video_id = extract_video_id(url_or_id) if "youtube.com" in url_or_id or "youtu.be" in url_or_id else url_or_id
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

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append([
                comment["authorDisplayName"],
                comment["publishedAt"],
                comment["updatedAt"],
                comment["likeCount"],
                comment["textDisplay"]
            ])
        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return pd.DataFrame(comments, columns=["author", "published_at", "updated_at", "like_count", "text"])

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
    df = pd.DataFrame(cleaned_comments, columns=["text"])
    analyzer = SentimentIntensityAnalyzer()

    sentiment_scores = []

    for comment_token in df["text"]:
        sentiment = analyzer.polarity_scores(comment_token)
        sentiment_scores.append(sentiment)

    return sentiment_scores

def get_sentiment_over_time(url_or_id):
    comments_df = fetch_youtube_comments(url_or_id)
    sentiments = analyze_sentiment(comments_df['text'])
    results_df = pd.DataFrame({
        'timestamp': comments_df['published_at'],
        'sentiment': [sent['compound'] for sent in sentiments]
    })
    
    return results_df
