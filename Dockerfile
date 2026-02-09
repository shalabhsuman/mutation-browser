FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend /app/backend

# Expose Flask port
EXPOSE 5000

# Run the Flask app
# CMD ["python", "backend/app.py"]
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "backend.app:app"]