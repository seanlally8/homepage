# This will be the sript for sorting emails for subscription

import os
import re
import sqlite3
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# initialize list to store incoming emails
email_list = []

# Define function that tests emails for appropriate format (abc@hotmail.com or abc@gmail.co.uk or abc@university.edu etc)
def validate_email(email):
    pattern = r'^[a-zA-Z0-9.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Define function to send confirmation email upon subscription
def send_confirmation_email(to_email):
    # Your Gmail credentials
    sender_email = "seanlally8@gmail.com"
    app_password = "ypqk fcif vytv cnfn"  # NOT your Gmail password

    # Email content
    subject = "Subscription Confirmed"
    body = "Hey! You made it! Now we can be best friends foreverrrrr."

    # Set up MIME structure
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, message.as_string())
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

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    origin = request.form.get('origin', '/')
    template_name = origin.strip('/') or 'index'

    if not validate_email(email):
        return render_template(f"{template_name}.html", show_badformat_modal=True)

    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL
        )
    ''')

    try:
        cursor.execute('INSERT INTO emails (email) VALUES (?)', (email,))
        conn.commit()
        send_confirmation_email(email)
        return render_template(f"{template_name}.html", show_success_modal=True)

    except sqlite3.IntegrityError:
        return render_template(f"{template_name}.html", show_already_subscribed_modal=True)

    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

