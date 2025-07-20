from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import os

# MySQL connection
load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Query average likes per video
query = """
SELECT video_title, likes
FROM video_stats
WHERE likes IS NOT NULL
ORDER BY likes DESC
LIMIT 5;
"""
df = pd.read_sql(query, conn)
conn.close()

# Plot
plt.figure(figsize=(10,6))
plt.barh(df['video_title'], df['likes'], color='skyblue', edgecolor='black')
plt.xlabel('Average Likes')
plt.title('Top 5 Liked Videos')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('/Users/swethasriguttula/youtube_project/top_liked_videos.png')  # 🖼️ Saves as PNG
plt.show()
