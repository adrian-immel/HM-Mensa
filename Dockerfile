# Use an official Python runtime as a parent image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install FastWSGI for production
RUN pip install --no-cache-dir fastwsgi

# Copy the project files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Set environment variables
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application with FastWSGI
CMD ["python", "-m", "fastwsgi.cli", "--app", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
