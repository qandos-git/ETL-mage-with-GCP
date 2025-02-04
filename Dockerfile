# Use the latest stable Python version with a lightweight base image
FROM python:3.11-slim-bookworm

# Allow statements and log messages to appear immediately
ENV PYTHONUNBUFFERED True

# Set up the working directory
ENV APP_HOME /back-end
WORKDIR $APP_HOME

# Copy only required files first to optimize caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . ./

# Expose the default Cloud Run port
EXPOSE 8080

# Start the Gunicorn server
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 8 --timeout 0 app:app
