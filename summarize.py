from dotenv import load_dotenv
import pandas as pd
import mysql.connector
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

query = """
        SELECT video_title, video_id, published_date, views, likes, comments
        FROM video_stats
        ORDER BY views DESC
        LIMIT 5;
"""

df = pd.read_sql(query, conn)
print("Top 5 most watched videos:")
print(df)
print("\n")

cursor.execute("SELECT SUM(views) FROM video_stats;")
total_views = cursor.fetchone()[0]
print(f"📈 Total Views: {total_views}")

# --- 3. Most Recent Video Uploaded ---
cursor.execute("""
SELECT video_title, published_date 
FROM video_stats 
ORDER BY published_date DESC 
LIMIT 1;
""")
latest_video = cursor.fetchone()
print(f"🕒 Latest Video: {latest_video[0]} (Published: {latest_video[1]})")

# --- 4. Average Likes per Video ---
cursor.execute("SELECT AVG(likes) FROM video_stats;")
avg_likes = cursor.fetchone()[0]
print(f"💖 Average Likes: {int(avg_likes)}")

conn.close()

