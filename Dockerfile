FROM python:3.11-slim
WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application, test configuration, docs, notebooks, and pre-compiled frontend distribution
COPY backend /app/backend
COPY pytest.ini /app/pytest.ini
COPY frontend/dist /app/frontend/dist
COPY docs /app/docs
COPY notebooks /app/notebooks

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1
EXPOSE 10000 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
