FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY server.py .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Optional environment variables
ENV INTELICA_BASE_URL=https://api.intelica.dev
ENV EVM_PRIVATE_KEY=""

# Expose port for Streamable HTTP
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=5)" || exit 1

# Start server
CMD ["python", "server.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
