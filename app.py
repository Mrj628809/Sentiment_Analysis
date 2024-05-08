from flask import Flask, request, jsonify, send_from_directory
import sentiment_analyzer as sa

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/analyze_comments", methods=["POST"])
def analyze_comments():
    content = request.get_json()
    url_or_id = content["video_url"]

    # Fetch comments and analyze sentiment
    comments_df = sa.fetch_youtube_comments(url_or_id)
    sentiment_scores = sa.analyze_sentiment(comments_df["text"])
    sentiment_counts = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }

    for score in sentiment_scores:
        compound = score["compound"]
        if compound > 0.0:
            sentiment_counts["Positive"] += 1
        elif compound < 0.0:
            sentiment_counts["Negative"] += 1
        else:
            sentiment_counts["Neutral"] += 1

    return jsonify({
        "sentiment_scores": sentiment_scores,
        "sentiment_counts": sentiment_counts
    })

if __name__ == "__main__":
    app.run(debug=True)
