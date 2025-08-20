# Use the official Alpine base image
FROM python:3.12-alpine

# Set the working directory
WORKDIR /home

COPY . /home

EXPOSE 5000

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install vim and other dependencies
RUN apk update && apk add --no-cache dos2unix \ 
    vim \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
	sqlite \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-base gcc musl-dev libffi-dev \
	&& dos2unix /home/start.sh \
	&& wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-amd64.zip && \
    unzip ngrok-stable-linux-amd64.zip && \
    mv ngrok /usr/local/bin && \
    chmod +x /usr/local/bin/ngrok && \
    rm ngrok-stable-linux-amd64.zip \
	&& ngrok config add-authtoken 31WTQem003GAmwsi40001rKkHI5_52A2aBKnS4sn9P6S59Qhh

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0

# Start Flask and ngrok together using a shell script
RUN chmod +x start.sh

CMD ["sh", "start.sh"]
