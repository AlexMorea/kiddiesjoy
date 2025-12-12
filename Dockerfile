# Use a small official Python runtime image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in container
WORKDIR /app

# Install system dependencies needed by psycopg2 and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (speeds up rebuilds when only app code changes)
COPY requirements.txt /app/

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /app

# Collect static files into /app/staticfiles (uses STATIC_ROOT from settings)
RUN python manage.py collectstatic --noinput || true

# Expose port (only informational)
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "kiddiesjoy.wsgi:application", "--bind", "0.0.0.0:8000"]
