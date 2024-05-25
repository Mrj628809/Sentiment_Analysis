# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt stopwords wordnet averaged_perceptron_tagger vader_lexicon

# Expose port 5001 for the Flask app
EXPOSE 5001

# Define environment variables
ENV FLASK_APP=app.py
#ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Health check command
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s CMD curl -f http://localhost:5001/health || exit 1
