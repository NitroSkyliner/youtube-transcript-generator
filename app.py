from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
import os
import re

app = Flask(__name__)

# Function to extract video ID from both regular and short-form URLs
def extract_video_id(url):
    # Regex for standard YouTube videos (https://www.youtube.com/watch?v=VIDEO_ID)
    standard_video_pattern = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|(?:.*[?&]v=))([^\"&?\/\n\s]{11}))"
    
    # Regex for YouTube Shorts (https://www.youtube.com/shorts/VIDEO_ID)
    short_video_pattern = r"^(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([^\"&?\/\n\s]{11})"

    # Match for standard YouTube video
    match_standard = re.match(standard_video_pattern, url)
    
    # Match for YouTube Shorts video
    match_short = re.match(short_video_pattern, url)

    if match_standard:
        return match_standard.group(1)  # Return the video ID for standard videos
    elif match_short:
        return match_short.group(1)  # Return the video ID for Shorts videos
    else:
        return None  # Return None if the URL is invalid

# Function to fetch transcript (no timestamps)
def get_transcript(video_id):
    try:
        # Get all available languages for the video
        available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        # Fetch the transcript in English (or fallback to English)
        transcript = available_transcripts.find_transcript(['en'])
        transcript_data = transcript.fetch()

        # Extract only the text (no timestamps)
        formatted_transcript = [entry['text'] for entry in transcript_data]
        return formatted_transcript
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    video_url = ""
    video_id = ""  # To store the extracted video ID

    if request.method == "POST":
        video_url = request.form["video_url"]
        # Extract video ID from the URL
        video_id = extract_video_id(video_url)
        if video_id:
            # Get the transcript for the extracted video ID
            transcript = get_transcript(video_id)
        else:
            transcript = "Invalid YouTube video URL or no video found."
    
    return render_template("index.html", transcript=transcript, video_url=video_url)

if __name__ == "__main__":
    app.run(debug=True)
