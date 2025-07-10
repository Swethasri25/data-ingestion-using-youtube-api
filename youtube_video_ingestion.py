from dotenv import load_dotenv
import requests
import pandas as pd
import re
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = 'UCq9kaXFyF2b6oXQ5veWdvog'  # Netflix

# 1. Get video IDs from the channel
search_url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=10'

search_response = requests.get(search_url)
search_data = search_response.json()
# print(search_data)

video_ids = []
for item in search_data['items']:
    if item['id']['kind'] == 'youtube#video':
        video_ids.append(item['id']['videoId'])

# 2. Fetch video stats using video IDs
video_stats_url = f'https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={",".join(video_ids)}&part=snippet,statistics'
video_response = requests.get(video_stats_url)
video_data = video_response.json()

# 3. Extract relevant fields
video_info_list = []
for video in video_data['items']:
    snippet = video['snippet']
    stats = video['statistics']
    
    video_info = {
        'Video Title': snippet['title'],
        'Video ID': video['id'],
        'Published Date': snippet['publishedAt'],
        'Views': stats.get('viewCount'),
        'Likes': stats.get('likeCount'),
        'Comments': stats.get('commentCount')
    }
    video_info_list.append(video_info)

# 4. Save to CSV
df = pd.DataFrame(video_info_list)
# df.index += 1
# print(df)
df.to_csv('video_stats.csv', index=True)

df_vs = pd.read_csv('video_stats.csv')

def clean_text(text):
    if pd.isnull(text):
        return ""
    return re.sub(r'[^\w\s|]', '', text)  # keeps letters, numbers, space, and pipe "|"

df_vs['Video Title'] = df_vs['Video Title'].apply(clean_text)

df_vs.dropna(how='all', inplace=True)

df_vs.to_csv('cleaned_video_stats.csv', index=False)

print(df_vs)

print("✅ Video stats saved to video_stats.csv")
# print(df.head())