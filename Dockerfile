# Use the official Alpine base image
FROM python:3.12-alpine

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install vim and other dependencies
RUN apk update && apk add --no-cache \
    vim \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
	sqlite \
    && pip install --upgrade pip \
    && pip install flask openpyxl \
    && apk del build-base gcc musl-dev libffi-dev

# Set the working directory
WORKDIR /home

COPY . /home

EXPOSE 5000

# Copy application code (if any) into the container
# COPY . /app

# Default command: open a shell instead of python
CMD ["/bin/sh"]
