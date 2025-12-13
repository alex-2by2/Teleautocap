from flask import Flask, render_template, request, redirect, session, url_for
import os
from db import channels

app = Flask(__name__)
app.secret_key = "super-secret-key"  # change later

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            session["admin"] = True   # ✅ LOGIN SAVED
            return redirect(url_for("dashboard"))

        return "❌ Wrong Password"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))

    return render_template("dashboard.html", channels=channels.find())

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

# ---------------- RUN ----------------
app.run(host="0.0.0.0", port=8080)
