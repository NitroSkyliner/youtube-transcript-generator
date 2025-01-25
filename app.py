from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
import os
import re

app = Flask(__name__)

# Function to extract video ID from both regular and short-form URLs
def extract_video_id(url):
    standard_video_pattern = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|(?:.*[?&]v=))([^\"&?\/\n\s]{11}))"
    short_video_pattern = r"^(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([^\"&?\/\n\s]{11})"

    match_standard = re.match(standard_video_pattern, url)
    match_short = re.match(short_video_pattern, url)

    if match_standard:
        return match_standard.group(1)
    elif match_short:
        return match_short.group(1)
    else:
        return None

# Function to fetch transcript (no timestamps)
# Function to fetch transcript (no timestamps)
def get_transcript(video_id):
    try:
        available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = available_transcripts.find_transcript(['en'])
        transcript_data = transcript.fetch()
        formatted_transcript = [entry['text'] for entry in transcript_data]
        return formatted_transcript
    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error for better visibility
        return f"Error fetching transcript: {str(e)}"


# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    video_url = ""
    video_id = ""  # To store the extracted video ID

    if request.method == "POST":
        video_url = request.form["video_url"]
        video_id = extract_video_id(video_url)
        if video_id:
            transcript = get_transcript(video_id)
        else:
            transcript = "Invalid YouTube video URL or no video found."
    
    return render_template("index.html", transcript=transcript, video_url=video_url)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
