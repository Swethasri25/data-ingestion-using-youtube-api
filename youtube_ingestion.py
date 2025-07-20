from dotenv import load_dotenv
from channel_id import get_channel_id_from_video
import requests
import pandas as pd
import os

load_dotenv()

# Replace with your actual API key
API_KEY = os.getenv("YOUTUBE_API_KEY")
video_url = "https://www.youtube.com/watch?v=1vPPnZggrkw&ab_channel=AyeJude"
CHANNEL_ID = get_channel_id_from_video(video_url)  # Aye Jude example UCq9kaXFyF2b6oXQ5veWdvog

if CHANNEL_ID:
    print(f"✅ Fetched Channel ID: {CHANNEL_ID}")
    # You can now use this channel_id for further API calls
else:
    print("❌ Channel ID not found")

url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={CHANNEL_ID}&key={API_KEY}"

response = requests.get(url)
data = response.json()

# Extract fields
if 'items' in data:
    channel_data = data['items'][0]
    snippet = channel_data['snippet']
    stats = channel_data['statistics']

    info = {
        'Channel Title': snippet['title'],
        'Subscribers': stats.get('subscriberCount'),
        'Total Views': stats.get('viewCount'),
        'Video Count': stats.get('videoCount'),
        'Country': snippet.get('country', 'N/A')
    }

    df = pd.DataFrame([info])
    print(df)

    # Save to CSV
    df.to_csv('channel_stats.csv', index=False)
    print("✅ Data saved to channel_stats.csv")
else:
    print("❌ Error fetching channel data")
