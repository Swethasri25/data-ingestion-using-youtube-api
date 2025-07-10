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

