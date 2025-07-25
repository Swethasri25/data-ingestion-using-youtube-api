from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import os

# Read CSV data
df = pd.read_csv('cleaned_video_stats.csv')

df['Published Date'] = pd.to_datetime(df['Published Date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

load_dotenv()

# Connect to MySQL
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

df = df.dropna(subset=['Video Title', 'Video ID'])

# Insert data
for _, row in df.iterrows():
    if pd.isnull(row['Video Title']) or pd.isnull(row['Video ID']):
        continue
    sql = """
        INSERT INTO video_stats (video_title, video_id, published_date, views, likes, comments)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            views = VALUES(views),
            likes = VALUES(likes),
            comments = VALUES(comments);
    """
    values = (
        row['Video Title'],
        row['Video ID'],
        row['Published Date'],
        int(row['Views']) if pd.notnull(row['Views']) else None,
        int(row['Likes']) if pd.notnull(row['Likes']) else None,
        int(row['Comments']) if pd.notnull(row['Comments']) else None
    )
    cursor.execute(sql, values)

conn.commit()
cursor.close()
conn.close()

print("✅ Data loaded into MySQL successfully!")
