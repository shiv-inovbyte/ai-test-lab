FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY deployment/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy core application files
COPY app.py ./
COPY verity_assistant_ai_llm.py ./
COPY verity_assistant_ai.py ./
COPY verity_pt_model.py ./
COPY utils.py ./
COPY generate_data.py ./
COPY engineer_feature.py ./
COPY save_model.py ./

# Copy model and configuration files
COPY model.joblib ./
COPY model_features.json ./

# Note: Add .env file manually or via docker run -v if needed for OPENAI_API_KEY

# Expose port (updated to match app.py default)
EXPOSE 6000

# Environment variables
ENV MODEL_PATH=/app/model.joblib
ENV PORT=6000
ENV FLASK_DEBUG=false

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:6000/health || exit 1

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:6000", "app:app", "--workers", "2", "--timeout", "120"]
