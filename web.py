from flask import Flask, render_template, request, redirect, session, url_for
import os
from db import channels

app = Flask(__name__)

# 🔐 Session secret key (required)
app.secret_key = "change-this-secret-key"

# 🔑 Admin password from Railway Variables
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# ---------------- LOGIN PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        if ADMIN_PASSWORD is None:
            return "❌ ADMIN_PASSWORD not set in Railway Variables"

        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            return "❌ Wrong Password"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))

    all_channels = list(channels.find())
    return render_template("dashboard.html", channels=all_channels)


# ---------------- ADD CHANNEL ----------------
@app.route("/add-channel", methods=["POST"])
def add_channel():
    if not session.get("admin"):
        return redirect(url_for("login"))

    channel_id = request.form.get("channel_id")

    if not channel_id:
        return "❌ Channel ID required"

    # Avoid duplicate channel
    if channels.find_one({"channel_id": int(channel_id)}):
        return "⚠️ Channel already exists"

    channels.insert_one({
        "channel_id": int(channel_id),
        "photo_caption": request.form.get("photo_caption", "📸 Photo"),
        "video_caption": request.form.get("video_caption", "🎥 Video"),
        "footer": request.form.get("footer", "Join @channel"),
        "template": request.form.get("template", "{caption}"),
        "buttons": []
    })

    return redirect(url_for("dashboard"))


# ---------------- DELETE CHANNEL ----------------
@app.route("/delete-channel/<int:channel_id>")
def delete_channel(channel_id):
    if not session.get("admin"):
        return redirect(url_for("login"))

    channels.delete_one({"channel_id": channel_id})
    return redirect(url_for("dashboard"))


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
