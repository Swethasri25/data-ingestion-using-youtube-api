import requests
import os
from dotenv import load_dotenv
from channel_id import get_channel_id_from_video

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
video_url = "https://www.youtube.com/watch?v=1vPPnZggrkw&ab_channel=AyeJude"
CHANNEL_ID = get_channel_id_from_video(video_url)  # Replace this with actual channel ID

MAX_RESULTS = 50
video_ids = []
next_page_token = None

while len(video_ids) < 100:
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"key={API_KEY}&channelId={CHANNEL_ID}&part=snippet"
        f"&order=date&type=video&maxResults={MAX_RESULTS}"
    )
    if next_page_token:
        url += f"&pageToken={next_page_token}"
        print("Next Page Token:", next_page_token)

    response = requests.get(url)
    data = response.json()

    for item in data.get("items", []):
        video_ids.append(item["id"]["videoId"])

    next_page_token = data.get("nextPageToken")
    if not next_page_token:
        break

print(f"✅ Total video IDs fetched: {len(video_ids)}")
print(video_ids)  # Optional: Check what you got
