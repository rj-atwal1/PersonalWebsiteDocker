# Use an official lightweight Python image.
FROM python:3.11-slim

# Do not buffer stdout/stderr, and disable generation of .pyc files.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create and switch to the working directory.
WORKDIR /app

# Install Python dependencies first to benefit from Docker layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container.
COPY . .

# Environment configuration for Flask.
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    FLASK_ENV=production

# Expose the Flask development server port.
EXPOSE 5000

# Run the web application.
CMD ["flask", "run"]
