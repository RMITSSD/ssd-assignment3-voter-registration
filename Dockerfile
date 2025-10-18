FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir watchdog

# Copy app
COPY . .

# Env for Flask CLI
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app:create_app
ENV FLASK_DEBUG=1

# Expose port
EXPOSE 5000

# Default: dev server with reload
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
