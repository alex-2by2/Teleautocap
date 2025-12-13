from flask import Flask, request, redirect, session, url_for, render_template
import os

app = Flask(__name__)
app.secret_key = "secret-key"

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        return "Wrong Password"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return "<h2>Dashboard Working ✅</h2><a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

app.run(host="0.0.0.0", port=8080)
