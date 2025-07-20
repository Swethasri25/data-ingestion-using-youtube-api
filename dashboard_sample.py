import streamlit as st
import pandas as pd

# Load cleaned CSV
df = pd.read_csv('cleaned_video_stats.csv')

# Title
st.title("🎬 YouTube Channel Video Dashboard")

# Show dataset
st.subheader("📄 Video Data")
st.dataframe(df)

# Bar chart: Views per video
st.subheader("📊 Views per Video")
df['Views'] = df['Views'].astype(int)
st.bar_chart(df.set_index('Video Title')['Views'])

# Filter by threshold
st.subheader("🔍 Filter by Minimum Views")
min_views = st.slider("Minimum number of views", 0, df['Views'].max(), 1000)
filtered = df[df['Views'] >= min_views]
st.write(f"Showing {len(filtered)} videos with more than {min_views} views")
st.dataframe(filtered)
