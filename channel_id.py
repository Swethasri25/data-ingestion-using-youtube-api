import requests
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_channel_id_from_video(video_url):
    # Extract video ID from URL
    parsed_url = urlparse(video_url)
    video_id = parse_qs(parsed_url.query).get("v", [None])[0]

    if not video_id:
        print("❌ Invalid video URL")
        return None

    # Call YouTube API to get video details
    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
    response = requests.get(api_url)
    data = response.json()

    try:
        channel_id = data["items"][0]["snippet"]["channelId"]
        channel_title = data["items"][0]["snippet"]["channelTitle"]
        print(f"✅ Channel ID: {channel_id} ({channel_title})")
        return channel_id
    except IndexError:
        print("❌ Video not found or API error")
        return None

# Example
# video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_url = "https://www.youtube.com/watch?v=1vPPnZggrkw&ab_channel=AyeJude"
get_channel_id_from_video(video_url)
