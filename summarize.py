import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root12345',
    database = 'youtube_data'
)

query = """
        SELECT video_title, video_id, published_date, views, likes, comments
        FROM video_stats
        ORDER BY views DESC
        LIMIT 5;
"""

df = pd.read_sql(query, conn)

print("Top 5 most watched videos:")
print(df)

conn.close()

