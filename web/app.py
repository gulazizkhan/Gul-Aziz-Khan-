from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from pathlib import Path
import csv

app = Flask(__name__)
app.secret_key = "gul-aziz-khan-demo-secret"

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)
MESSAGES = DATA / "messages.csv"

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/contact")
def contact():
    name = request.form.get("name","").strip()
    email = request.form.get("email","").strip()
    subject = request.form.get("subject","").strip()
    message = request.form.get("message","").strip()
    if not name or not email or not message:
        flash("Please fill in the required fields.", "error")
        return redirect(url_for("home") + "#contact")
    new = not MESSAGES.exists()
    with MESSAGES.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["date","name","email","subject","message"])
        w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),name,email,subject,message])
    flash("Your message has been received. Thank you!", "success")
    return redirect(url_for("home") + "#contact")

@app.route("/admin/messages")
def messages():
    rows = []
    if MESSAGES.exists():
        with MESSAGES.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    return render_template("messages.html", messages=rows)

if __name__ == "__main__":
    app.run(debug=True)
