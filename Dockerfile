# Dockerfile para Servidor de Análisis de Exposición de Datos - Edición Revelada (Español)
# Basado en Python 3.11 slim para un contenedor ligero y seguro

FROM python:3.11-slim

# Información del mantenedor
LABEL maintainer="Cybersecurity Education Team"
LABEL description="Servidor educativo de análisis de exposición de datos personales"
LABEL version="2.0"
LABEL language="español"

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=server_revelado.py \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    PORT=5000

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /bin/bash appuser

# Instalar dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        netcat-traditional && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY server_revelado.py .
COPY startup.sh .

# Crear directorio para logs y hacer el script ejecutable
RUN mkdir -p /app/logs && \
    chmod +x /app/startup.sh && \
    chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 5000

# Verificación de salud del contenedor
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/salud || exit 1

# Comando por defecto
CMD ["./startup.sh"]
