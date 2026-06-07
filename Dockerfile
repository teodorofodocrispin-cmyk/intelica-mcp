FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends     gcc     && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY pyproject.toml .
COPY server.py .

# Instalar dependencias
RUN pip install --no-cache-dir -e .

# Variables de entorno opcionales
ENV INTELICA_BASE_URL=https://intelica.onrender.com
ENV EVM_PRIVATE_KEY=""

# Exponer puerto para Streamable HTTP
EXPOSE 8000

# Comando de inicio
CMD ["python", "server.py"]
