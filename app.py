import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_this'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'messages.json')

def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def save_messages(messages):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not name or not email or not message:
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('home'))

    messages = load_messages()
    messages.append({
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    })
    save_messages(messages)

    flash('Thank you for your message! I will get back to you soon.', 'success')
    return redirect(url_for('home'))

@app.route('/admin/messages')
def view_messages():
    messages = load_messages()
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=False)
