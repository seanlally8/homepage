# This will be the sript for sorting emails for subscription

import os
import re

from flask import Flask, render_template, request
from openpyxl import Workbook, load_workbook

app = Flask(__name__)

# initialize list to store incoming emails
email_list = []

# Define function that tests emails for appropriate format (abc@hotmail.com or abc@gmail.co.uk or abc@university.edu etc)
def validate_email(email):
    pattern = r'^[a-zA-Z0-9.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/', methods=['GET','POST'])
def form():
    email = None
    if request.method == 'POST':
        email = request.form.get('email')
        
        for item in email_list:
            if email == item:
                print("already subscribed")
                email = None
                return render_template('index_alreadysubscribed.html')

        if validate_email(email):  
            email_list.append(email)
            email_list.sort()
            print(email_list)
            print("success")
            return render_template('index_success.html')
        else:
            print("failure")
            return render_template('index_badformat.html')
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

