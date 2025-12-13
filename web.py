from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>Admin Panel Running ✅</h2>"

@app.route("/dashboard")
def dashboard():
    return "<h2>Admin Panel Running ✅</h2>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # 🔥 IMPORTANT
    app.run(host="0.0.0.0", port=port)
