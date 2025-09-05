#!/bin/bash
# Startup script para Servidor de Análisis de Exposición de Datos
# Versión: 2.0 - Edición Revelada (Español)

set -e

echo "🕵️ Iniciando Servidor de Análisis de Exposición de Datos..."
echo "📅 Fecha: $(date)"
echo "🐳 Contenedor: $(hostname)"
echo "👤 Usuario: $(whoami)"
echo "📁 Directorio: $(pwd)"

# Verificar archivos necesarios
if [ ! -f "server_revelado.py" ]; then
    echo "❌ Error: No se encuentra server_revelado.py"
    exit 1
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Mostrar información del entorno
echo "🔧 Variables de entorno:"
echo "   FLASK_ENV: ${FLASK_ENV:-production}"
echo "   FLASK_DEBUG: ${FLASK_DEBUG:-0}"
echo "   PORT: ${PORT:-5000}"

# Verificar conectividad de red (opcional)
if command -v curl >/dev/null 2>&1; then
    echo "🌐 Verificando conectividad..."
    if curl -s --max-time 5 http://ip-api.com/json/1.1.1.1 >/dev/null; then
        echo "✅ Conectividad a servicios externos: OK"
    else
        echo "⚠️  Advertencia: Sin conectividad a servicios externos"
        echo "   Las funciones de geolocalización IP pueden no funcionar"
    fi
fi

# Mostrar información de Python
echo "🐍 Python: $(python --version)"
echo "📦 Paquetes instalados:"
pip list | grep -E "(Flask|requests)" || true

echo "🚀 Iniciando servidor Flask..."
echo "📡 Acceso: http://localhost:${PORT:-5000}"
echo "🛡️ Estado: http://localhost:${PORT:-5000}/salud"
echo "=" * 60

# Ejecutar la aplicación
exec python server_revelado.py
