from flask import Flask, request, redirect, session, url_for
import os

app = Flask(__name__)

# 🔐 session key (any random string)
app.secret_key = "super-secret-login-key"

# 🔑 admin password from Railway Variables
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            return "<h3>❌ Wrong Password</h3><a href='/'>Try again</a>"

    return """
    <h2>Admin Login
