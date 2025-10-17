FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

EXPOSE 8000

ENV MODEL_PATH=/app/verity-AI/model.joblib

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers", "2"]
