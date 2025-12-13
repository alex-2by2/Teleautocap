
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from db import schedules, channels

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

def run_daily():
    now = datetime.now().strftime("%H:%M")
    for s in schedules.find({"type": "daily", "time": now, "active": True}):
        channels.update_one(
            {"channel_id": s["channel_id"]},
            {"$set": {
                "photo_caption": s["photo_caption"],
                "video_caption": s["video_caption"],
                "footer": s["footer"],
                "template": s["template"]
            }}
        )

scheduler.add_job(run_daily, "interval", minutes=1)
scheduler.start()
