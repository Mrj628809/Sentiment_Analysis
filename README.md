# YouTube Sentiment Analyzer

This project is a Dockerized Flask application that analyzes the sentiment of YouTube video comments. It fetches comments from YouTube videos, processes them using VADER and NLTK for sentiment analysis, and provides insightful visualizations, including sentiment distribution and trends over time.

### Table of Contents
1. [Installation Instructions](#installation-instructions)
2. [Usage Guide](#usage-guide)
3. [API Documentation](#api-documentation)
4. [Contribution Guidelines](#contribution-guidelines)

---

### Installation Instructions

#### Prerequisites
- Docker installed on your machine
- YouTube Data API key

#### Steps
1. **Clone the Repository**

   Clone the project repository to your local machine:
   ```sh
   git clone https://github.com/Mrj628809/Sentiment_Analysis.git
   cd Sentiment_Analysis
   ```

2. **Set Up Environment Variables**

   Create a `.env` file in the project root directory and add your YouTube Data API key:
   ```sh
   echo "DEVELOPER_KEY=your_api_key_here" > .env
   ```

3. **Build and Run the Docker Container**

   Build the Docker image:
   ```sh
   docker build -t youtube-sentiment-analyzer .
   ```

   Run the Docker container:
   ```sh
   docker run -d -p 5000:5000 --env-file .env youtube-sentiment-analyzer
   ```

4. **Access the Application**

   Open your web browser and go to `http://localhost:5000`.

---

### Usage Guide

1. **Home Page**

   When you visit the application at `http://localhost:5000`, you'll see the home page with a form to enter the YouTube video URL.

2. **Analyze Comments**

   Enter the YouTube video URL and click "Analyze". The application will fetch comments from the video, analyze their sentiment, and display visualizations:
   - Pie chart showing the distribution of positive, negative, and neutral comments.
   - Bar chart showing the sentiment counts.
   - Heat map showing sentiment over time.

---

### API Documentation

#### `/analyze_comments` (POST)

- **Description**: Analyzes the sentiment of comments for a given YouTube video URL.
- **Request Body**: JSON object containing the video URL.
  ```json
  {
    "video_url": "https://www.youtube.com/watch?v=example_video_id"
  }
  ```
- **Response**: JSON object containing sentiment scores, sentiment counts, and sentiment over time.
  ```json
  {
    "sentiment_scores": [{...}],
    "sentiment_counts": {
      "Positive": 23,
      "Negative": 5,
      "Neutral": 24
    },
    "sentiment_over_time": [{...}]
  }
  ```

---

### Contribution Guidelines

We welcome contributions from the community! Here are some guidelines to help you get started:

1. **Fork the Repository**

   Fork the project repository to your GitHub account.

2. **Create a Feature Branch**

   Create a branch for your feature or bug fix:
   ```sh
   git checkout -b feature-name
   ```

3. **Make Changes**

   Implement your feature or bug fix. Ensure your code follows the project's coding standards.

4. **Commit Changes**

   Commit your changes with a descriptive commit message:
   ```sh
   git commit -m "Add feature-name"
   ```

5. **Push to GitHub**

   Push your changes to your forked repository:
   ```sh
   git push origin feature-name
   ```

6. **Create a Pull Request**

   Create a pull request from your feature branch to the main repository. Describe your changes in detail.

---

Feel free to ask if you need any further assistance with any of these steps!
