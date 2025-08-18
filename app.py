# This will be the sript for sorting emails for subscription

import os

from flask import Flask, render_template, request
from openpyxl import Workbook, load_workbook

app = Flask(__name__)
EXCEL_FILE = 'emails.xlsx'

# Create Excel file with header if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    wb = Workbook()
    ws = wb.active
    ws.title = "Emails"
    ws.append(["Email"])  # Header row
    wb.save(EXCEL_FILE)


@app.route('/', methods=['GET','POST'])
def form():
    email = None
    if request.method == 'POST':
        email = request.form.get('email')

    if email:
        # Load existing Excel file
        wb = load_workbook(EXCEL_FILE)
        ws = wb.active

        # Append the new email
        ws.append([email])

        # Optional: Sort all emails alphabetically
        # Skip header row
        emails = [row[0] for row in ws.iter_rows(min_row=2, values_only=True)]
        emails = list(set(emails))  # Remove duplicates if needed
        emails.sort()

        # Clear and re-write sorted emails
        ws.delete_rows(2, ws.max_row)
        for e in emails:
            ws.append([e])

        wb.save(EXCEL_FILE)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

