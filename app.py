# This will be the sript for sorting emails for subscription

import os

from flask import Flask, render_template, request
from openpyxl import Workbook, load_workbook

app = Flask(__name__)
email_list = []

@app.route('/', methods=['GET','POST'])
def form():
    email = None
    if request.method == 'POST':
        email = request.form.get('email')

    if email:
       email_list.append(email)
       email_list.sort()
       print(email_list)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

