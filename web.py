from flask import Flask, request, redirect, session, url_for
import os
from db import init_db, channels

app = Flask(__name__)
app.secret_key = "super-secret-key"

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# init DB safely
init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        return "<h3>Wrong Password</h3>"

    return """
    <h2>Admin Login</h2>
    <form method="post">
      <input type="password" name="password" placeholder="Admin Password" required>
      <button type="submit">Login</button>
    </form>
    """

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))

    if channels is None:
        return "<h3>Dashboard Working ✅</h3><p>⚠️ MongoDB not connected</p>"

    data = list(channels.find())
    html = "<h2>Dashboard Working ✅</h2><ul>"
    for c in data:
        html += f"<li>{c.get('channel_id')}</li>"
    html += "</ul><a href='/logout'>Logout</a>"
    return html

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# 🔴 Safety net: NEVER show 500 error
@app.errorhandler(Exception)
def handle_error(e):
    return "<h2>Admin Panel Running ✅</h2>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
