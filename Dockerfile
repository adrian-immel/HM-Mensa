FROM python:3.9-slim

LABEL authors="Adrian Immel"

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /src

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "your_app:ap