# This will be the sript for sorting emails for subscription

import os
import re
import sqlite3
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash

# Global constants
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Better: generates a secure random key each run

load_dotenv()  # load variables from .env

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))

# Define function that tests emails for appropriate format (abc@hotmail.com or abc@gmail.co.uk or abc@university.edu etc)
def validate_email(email):
    pattern = r'^[a-zA-Z0-9.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Define function to send confirmation email upon subscription
def send_confirmation_email(to_email):
    # Email content
    subject = "Subscription Confirmed"
    body = "Hey! You made it! Now we can be best friends foreverrrrr."

    # Set up MIME structure
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, message.as_string())
        server.quit()
        print(f"Confirmation email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    origin = request.form.get('origin', '/')
    template_name = origin.strip('/') or 'index'


    if not validate_email(email):
        flash('badformat')
        return redirect(origin)

    try:
        conn = sqlite3.connect('emails.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL
            )
        ''')

        cursor.execute('INSERT INTO emails (email) VALUES (?)', (email,))
        conn.commit()
        flash('success')
        send_confirmation_email(email)

    except sqlite3.IntegrityError:
        flash('already_subscribed')

    finally:
        conn.close()

    return redirect(origin)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

