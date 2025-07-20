import schedule
import time
import subprocess

# Define your job
def run_pipeline():
    # print(f"\n🚀 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running data pipeline...")

    try: 
        print("🚀 Running data pipeline...")
        # subprocess.run(["python3", "/Users/swethasriguttula/youtube_project/youtube_ingestion.py"])
        subprocess.run(["python3", "/Users/swethasriguttula/youtube_project/load_data.py"])
        subprocess.run(["python3", "/Users/swethasriguttula/youtube_project/youtube_video_ingestion.py"])
        subprocess.run(["python3", "/Users/swethasriguttula/youtube_project/summarize.py"])
        subprocess.run(["python3", "/Users/swethasriguttula/youtube_project/summary_graph.py"])
        
        print("✅ Pipeline run complete!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during pipeline execution: {e}")

run_pipeline()

# Schedule it every day at 10:00 AM
schedule.every().day.at("10:00").do(run_pipeline)

print("⏳ Waiting for scheduled time...")
while True:
    schedule.run_pending()
    time.sleep(60)
