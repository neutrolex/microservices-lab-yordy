FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY requirements-test.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements-test.txt

# Copiar el script de test
COPY test_connection.py .

# Mantener el contenedor corriendo
CMD ["tail", "-f", "/dev/null"]