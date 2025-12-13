
from flask import Flask, render_template, request, redirect
import os
from db import channels, schedules

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == os.getenv("ADMIN_PASSWORD"):
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", channels=channels.find())

@app.route("/add-channel", methods=["POST"])
def add_channel():
    channels.insert_one({
        "channel_id": int(request.form["channel_id"]),
        "photo_caption": "📸 Photo",
        "video_caption": "🎥 Video",
        "footer": "Join @channel",
        "template": "{caption}",
        "buttons": []
    })
    return redirect("/dashboard")

app.run(host="0.0.0.0", port=8080)
