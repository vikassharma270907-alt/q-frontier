# Stage 1: Frontend Build
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend Runtime
FROM python:3.11-slim
WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY backend /app/backend
COPY pytest.ini /app/pytest.ini

# Copy frontend distribution
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1
ENV PORT=10000
EXPOSE 10000 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
