# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn for production
RUN pip install --no-cache-dir gunicorn

# Copy the project files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Fix the path references in the code
RUN sed -i 's|../config.yml|/app/config.yml|g' /app/src/yaml_parser.py && \
    sed -i 's|../logs|/app/logs|g' /app/src/main.py

## declare volumes
VOLUME /app/logs
VOLUME /app/config.yml

# Set environment variables
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.main:app"]
