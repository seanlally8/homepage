#!/bin/bash

# Start Flask app in the background
python app.py &

# Wait for the Flask server to start
sleep 2

# Start ngrok and forward to port 5000
ngrok http 5000

