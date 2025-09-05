# 🐳 Servidor de Análisis de Exposición de Datos - Despliegue con Docker

## 📋 Descripción

Contenedor Docker para el **Servidor de Análisis de Exposición de Datos - Edición Revelada (Español)**, una herramienta educativa de ciberseguridad que demuestra qué información pueden recopilar los sitios web sobre los usuarios.

## 🚀 Inicio Rápido

### Opción 1: Docker Compose (Recomendado)

```bash
# Clonar o navegar al directorio del proyecto
cd cybersec-script

# Construir y ejecutar con Docker Compose
docker-compose up --build

# Acceder a la aplicación
# http://localhost:5000
```

### Opción 2: Docker directo

```bash
# Construir la imagen
docker build -t cybersec-demo:latest .

# Ejecutar el contenedor
docker run -d \
  --name cybersec-demo \
  -p 5000:5000 \
  --restart unless-stopped \
  cybersec-demo:latest

# Verificar que está funcionando
curl http://localhost:5000/salud
```

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `FLASK_ENV` | Entorno de Flask | `production` |
| `FLASK_DEBUG` | Modo debug | `0` (deshabilitado) |
| `PORT` | Puerto de la aplicación | `5000` |

### Ejemplo con variables personalizadas:

```bash
docker run -d \
  --name cybersec-demo \
  -p 8080:8080 \
  -e PORT=8080 \
  -e FLASK_ENV=development \
  cybersec-demo:latest
```

## 📊 Monitoreo y Salud

### Verificación de Salud

El contenedor incluye verificaciones de salud automáticas:

```bash
# Verificar estado del contenedor
docker ps

# Ver logs de salud
docker inspect --format='{{json .State.Health}}' cybersec-demo

# Verificar endpoint de salud manualmente
curl http://localhost:5000/salud
```

### Logs de la Aplicación

```bash
# Ver logs en tiempo real
docker logs -f cybersec-demo

# Ver últimas 100 líneas
docker logs --tail 100 cybersec-demo
```

## 🛠️ Comandos Útiles

### Gestión del Contenedor

```bash
# Detener el contenedor
docker stop cybersec-demo

# Reiniciar el contenedor
docker restart cybersec-demo

# Eliminar el contenedor
docker rm cybersec-demo

# Eliminar la imagen
docker rmi cybersec-demo:latest
```

### Con Docker Compose

```bash
# Iniciar en modo detached
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reconstruir y reiniciar
docker-compose up --build --force-recreate
```

## 📡 Endpoints Disponibles

Una vez ejecutándose, la aplicación expone:

- **`/`** - Página principal de demostración
- **`/analizar`** - Análisis completo de exposición de datos
- **`/consejos-privacidad`** - Guía completa de privacidad
- **`/salud`** - Estado del servicio (para healthchecks)
- **`/establecer-cookies-demo`** - Establecer cookies de demostración
- **`/limpiar-cookies`** - Eliminar cookies
- **`/prueba-huella-digital`** - Prueba de fingerprinting

## 🔒 Consideraciones de Seguridad

### Características de Seguridad Implementadas:

1. **Usuario no-root** - El contenedor ejecuta como usuario `appuser`
2. **Imagen base slim** - Reduce superficie de ataque
3. **Dependencias mínimas** - Solo paquetes necesarios
4. **Variables de entorno** - Configuración segura
5. **Health checks** - Monitoreo automático de salud

### Para Producción:

```bash
# Usar HTTPS reverso proxy (nginx/traefik)
# Configurar rate limiting
# Habilitar logging estructurado
# Usar secrets para configuración sensible
```

## 🌐 Acceso a la Aplicación

Después de ejecutar el contenedor:

1. **Abrir navegador** en `http://localhost:5000`
2. **Hacer clic** en "🔍 ESCANEAR MI EXPOSICIÓN DE DATOS"
3. **Revisar resultados** detallados en español
4. **Explorar consejos** de privacidad

## 🐛 Solución de Problemas

### El contenedor no inicia:

```bash
# Verificar logs
docker logs cybersec-demo

# Verificar puerto disponible
netstat -tulpn | grep 5000

# Verificar imagen construida
docker images | grep cybersec-demo
```

### Problemas de red:

```bash
# Verificar conectividad
docker exec cybersec-demo curl -f http://localhost:5000/salud

# Verificar puertos expuestos
docker port cybersec-demo
```

### Reconstruir completamente:

```bash
# Limpiar todo y reconstruir
docker-compose down --volumes --remove-orphans
docker system prune -f
docker-compose up --build
```

## 📈 Uso Educativo

Esta herramienta está diseñada para:

- **Capacitación en ciberseguridad**
- **Concientización sobre privacidad**
- **Demostraciones educativas**
- **Talleres de seguridad digital**

## ⚠️ Advertencias Importantes

- **Solo para educación** - No usar en producción sin medidas adicionales
- **Datos sensibles** - No ingresar información personal real
- **Red local** - Recomendado usar solo en redes controladas
- **Supervisión** - Usar bajo supervisión en entornos educativos

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear branch de feature
3. Commit con cambios
4. Push al branch
5. Crear Pull Request

## 📄 Licencia

Proyecto educativo de código abierto para concientización en ciberseguridad.

---

**🛡️ Recuerda: La privacidad es un derecho fundamental. Usa esta herramienta para educar y proteger.**
