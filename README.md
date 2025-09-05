# 🕵️ Servidor de Análisis de Exposición de Datos Personal

<div align="center">

![Cybersecurity](https://img.shields.io/badge/Security-Cybersecurity-red?style=for-the-badge&logo=shield)
![Educational](https://img.shields.io/badge/Purpose-Educational-blue?style=for-the-badge&logo=book)
![Spanish](https://img.shields.io/badge/Language-Spanish-yellow?style=for-the-badge&logo=spain)
![Docker](https://img.shields.io/badge/Deploy-Docker-blue?style=for-the-badge&logo=docker)
![Flask](https://img.shields.io/badge/Backend-Flask-green?style=for-the-badge&logo=flask)

### 🚨 **Herramienta Educativa de Ciberseguridad** 🚨

*Descubre EXACTAMENTE qué información pueden ver los sitios web sobre ti*

[🚀 Inicio Rápido](#-inicio-rápido) • [📖 Características](#-características) • [🐳 Docker](#-despliegue-con-docker) • [🛡️ Seguridad](#%EF%B8%8F-consideraciones-de-seguridad) • [📚 Uso Educativo](#-uso-educativo)

</div>

---

## 📋 Descripción del Proyecto

El **Servidor de Análisis de Exposición de Datos Personal** es una herramienta educativa avanzada diseñada para demostrar qué información personal pueden recopilar los sitios web sobre los usuarios sin su conocimiento explícito.

### 🎯 **Propósito Educativo**

Esta aplicación revela de manera **didáctica y segura** cómo los sitios web pueden:
- 📍 Rastrear tu ubicación aproximada
- 🔍 Crear huellas digitales únicas de tu dispositivo  
- 🍪 Almacenar y rastrear cookies de seguimiento
- 🌐 Analizar información del navegador y sistema operativo
- 👁️ Recopilar datos para perfilado publicitario

### ⚠️ **Advertencia Importante**

> **Este es un proyecto educativo diseñado para concientización en ciberseguridad.**  
> No recopila ni almacena datos personales reales. Toda la información se procesa localmente con fines demostrativos.

---

## ✨ Características

### 🔍 **Análisis Completo de Exposición**
- **Geolocalización por IP** - Ubicación aproximada basada en dirección IP
- **Fingerprinting del Navegador** - Identificación única del dispositivo
- **Análisis de Cookies** - Detección de cookies de seguimiento
- **Headers de Seguridad** - Evaluación de headers HTTP
- **Información del Sistema** - SO, navegador, idioma, zona horaria

### 📊 **Evaluación de Privacidad**
- **Puntuación de Privacidad** (0-100) con desglose detallado
- **Factores de Riesgo** identificados y explicados
- **Recomendaciones Personalizadas** para mejorar la privacidad
- **Resistencia a Fingerprinting** evaluada automáticamente

### 🛡️ **Educación en Ciberseguridad**
- **Explicaciones Detalladas** de cada tipo de dato recopilado
- **Consejos de Protección** específicos y accionables
- **Guías Paso a Paso** para configurar navegadores seguros
- **Herramientas Recomendadas** (VPNs, extensiones, navegadores)

### 🌐 **Interfaz Moderna**
- **100% en Español** para audiencia hispanohablante
- **Diseño Responsivo** para móviles y tablets
- **Interfaz Interactiva** con animaciones y feedback visual
- **Carga Dinámica** de contenido desde endpoints REST

---

## 🚀 Inicio Rápido

### 📋 Prerrequisitos

- **Docker** instalado ([Guía de instalación](https://docs.docker.com/get-docker/))
- **Make** (opcional, para comandos simplificados)
- **Git** para clonar el repositorio

### ⚡ Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/razeone/cybersec-script.git
cd cybersec-script

# 2. Construir y ejecutar con Docker
make build
make run

# 3. Acceder a la aplicación
# 🌐 http://localhost:5000
```

### 🐳 Con Docker (Manual)

```bash
# Construir imagen
docker build -t cybersec-demo:latest .

# Ejecutar contenedor
docker run -d \
  --name cybersec-demo \
  -p 5000:5000 \
  --restart unless-stopped \
  cybersec-demo:latest

# Verificar estado
curl http://localhost:5000/salud
```

### 🐍 Instalación Local (Python)

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar aplicación
python server_revelado.py

# 4. Acceder a http://localhost:5000
```

---

## 🐳 Despliegue con Docker

### 🛠️ Comandos del Makefile

```bash
# Gestión básica
make build     # Construir imagen Docker
make run       # Ejecutar contenedor
make stop      # Detener contenedor
make restart   # Reiniciar contenedor

# Monitoreo
make health    # Verificar estado de salud
make logs      # Ver logs en tiempo real
make info      # Información del contenedor

# Testing
make test      # Probar todos los endpoints
make dev       # Ejecutar en modo desarrollo
make prod      # Ejecutar en modo producción

# Limpieza
make clean     # Limpiar contenedores e imágenes
```

### 🔧 Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `FLASK_ENV` | Entorno de Flask | `production` |
| `FLASK_DEBUG` | Modo debug | `0` |
| `PORT` | Puerto de la aplicación | `5000` |

### 🐳 Docker Compose

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

---

## 📡 API Endpoints

### 🔍 **Principales**
- **`GET /`** - Página principal interactiva
- **`POST /analizar`** - Análisis completo de exposición de datos
- **`GET /salud`** - Estado de salud del servicio

### 📚 **Educativos**
- **`GET /consejos-privacidad`** - Guía completa de privacidad
- **`GET /reporte-privacidad`** - Reporte personalizado detallado
- **`GET /comparar-navegadores`** - Comparación de navegadores

### 🧪 **Demostrativos**
- **`GET /establecer-cookies-demo`** - Establecer cookies de demostración
- **`GET /limpiar-cookies`** - Eliminar todas las cookies
- **`GET /prueba-huella-digital`** - Test especializado de fingerprinting

### 📊 **Ejemplo de Respuesta API**

```json
{
  "direccion_ip": "127.0.0.1",
  "ubicacion": "Red Local, IP Privada, Local",
  "puntuacion_privacidad": 75,
  "riesgo_seguimiento": {
    "nivel": "MODERADO",
    "factores": ["Cookies presentes", "Headers de fingerprinting"]
  },
  "consejos_proteccion": [
    "Usar VPN para ocultar IP real",
    "Instalar bloqueadores de rastreadores"
  ]
}
```

---

## 🛡️ Consideraciones de Seguridad

### ✅ **Características de Seguridad Implementadas**

- **👤 Usuario No-Root** - El contenedor ejecuta como usuario `appuser`
- **🔒 Imagen Base Slim** - Superficie de ataque reducida
- **🏥 Health Checks** - Monitoreo automático de salud
- **📝 Logging Estructurado** - Trazabilidad de eventos
- **🌐 Headers de Seguridad** - Protección contra ataques comunes

### 🚨 **Limitaciones y Advertencias**

> ⚠️ **Para Uso Educativo Únicamente**
> - No usar en producción sin medidas adicionales de seguridad
> - No ingresar información personal real durante las demostraciones
> - Ejecutar solo en redes controladas y supervisadas
> - Ideal para entornos educativos y de capacitación

### 🔐 **Mejores Prácticas para Producción**

```bash
# Usar HTTPS con reverse proxy
# Implementar rate limiting
# Configurar firewall de aplicación
# Usar secrets management
# Habilitar logging de seguridad
```

---

## 📚 Uso Educativo

### 🎓 **Casos de Uso Ideales**

- **🏫 Instituciones Educativas** - Cursos de ciberseguridad
- **🏢 Capacitación Corporativa** - Concientización de empleados  
- **👨‍💼 Talleres Profesionales** - Formación en privacidad digital
- **🔒 Consultoría en Seguridad** - Demostraciones a clientes
- **📚 Cursos Online** - Material didáctico interactivo

### 📖 **Flujo de Aprendizaje Sugerido**

1. **🔍 Demostración Inicial** - Mostrar qué datos se exponen
2. **📊 Análisis de Resultados** - Explicar cada elemento detectado
3. **⚠️ Identificación de Riesgos** - Discutir implicaciones de privacidad
4. **🛡️ Consejos de Protección** - Implementar medidas de seguridad
5. **🔄 Verificación de Mejoras** - Comprobar efectividad de cambios

### 🎯 **Objetivos de Aprendizaje**

Al completar una sesión con esta herramienta, los usuarios podrán:

- ✅ **Comprender** qué datos exponen al navegar
- ✅ **Identificar** vectores de seguimiento y fingerprinting
- ✅ **Implementar** medidas básicas de protección
- ✅ **Evaluar** la efectividad de sus configuraciones de privacidad
- ✅ **Aplicar** buenas prácticas de seguridad digital

---

## 🔧 Desarrollo y Contribución

### 🏗️ **Estructura del Proyecto**

```
cybersec-script/
├── 📄 server_revelado.py      # Aplicación principal en español
├── 📄 server_revealed.py      # Versión en inglés
├── 📄 server_enhanced.py      # Versión mejorada base
├── 🐳 Dockerfile             # Configuración de contenedor
├── 🐳 docker-compose.yml     # Orquestación de servicios
├── 🛠️ Makefile              # Comandos de gestión
├── 📄 startup.sh             # Script de inicio
├── 📄 requirements.txt       # Dependencias Python
├── 📄 .gitignore            # Archivos excluidos de Git
└── 📚 README.md             # Este archivo
```

### 🤝 **Cómo Contribuir**

1. **Fork** el repositorio
2. **Crear branch** de feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** al branch (`git push origin feature/nueva-funcionalidad`)
5. **Crear Pull Request**

### 🐛 **Reportar Issues**

Si encuentras bugs o tienes sugerencias:
- 🔍 Verifica que no exista un issue similar
- 📝 Incluye pasos para reproducir el problema
- 💻 Especifica tu entorno (SO, navegador, etc.)
- 📋 Adjunta logs relevantes si es posible

---

## 📈 Versiones del Proyecto

### 🚀 **Versión Actual: 2.0 - Edición Revelada (Español)**

**Características principales:**
- ✅ Interfaz completamente en español
- ✅ Análisis detallado de exposición de datos
- ✅ Puntuación de privacidad con desglose
- ✅ Consejos educativos personalizados
- ✅ Containerización con Docker
- ✅ API REST completa

### 📊 **Roadmap Futuro**

- 🔄 **v2.1** - Análisis avanzado de WebRTC
- 🌐 **v2.2** - Soporte multi-idioma automático
- 📱 **v2.3** - PWA para dispositivos móviles
- 🔗 **v2.4** - Integración con herramientas de pentesting
- 📊 **v3.0** - Dashboard de administración

---

## 🆘 Solución de Problemas

### ❓ **Problemas Comunes**

<details>
<summary><strong>🐳 El contenedor no inicia</strong></summary>

```bash
# Verificar logs
docker logs cybersec-demo

# Verificar puerto disponible
netstat -tulpn | grep 5000

# Reconstruir imagen
make clean && make build
```
</details>

<details>
<summary><strong>🌐 Error de conectividad</strong></summary>

```bash
# Probar conectividad local
curl http://localhost:5000/salud

# Verificar firewall
sudo ufw status

# Verificar configuración de red Docker
docker network ls
```
</details>

<details>
<summary><strong>📊 Los datos no se muestran correctamente</strong></summary>

- Verificar que JavaScript esté habilitado
- Comprobar consola del navegador (F12)
- Probar en modo incógnito
- Verificar bloqueadores de anuncios
</details>

### 🔍 **Logs de Depuración**

```bash
# Ver logs en tiempo real
make logs

# Logs con timestamps
docker logs -t cybersec-demo

# Filtrar logs de error
docker logs cybersec-demo 2>&1 | grep ERROR
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la **Licencia MIT** con fines educativos.

```
MIT License - Uso Educativo en Ciberseguridad

Se permite el uso, copia, modificación y distribución de este software
para fines educativos y de concientización en ciberseguridad.

El software se proporciona "tal como está", sin garantías de ningún tipo.
```

---

## 🙏 Agradecimientos

- 🛡️ **Comunidad de Ciberseguridad** por las mejores prácticas
- 🐳 **Docker Community** por la containerización
- 🐍 **Flask Framework** por la base web robusta
- 📚 **Educadores en Seguridad** por la validación pedagógica

---

## 📞 Contacto y Soporte

### 💬 **Para Consultas Educativas**
- 📧 Abrir un [Issue en GitHub](https://github.com/razeone/cybersec-script/issues)
- 📚 Consultar la [documentación completa](./README_Docker.md)
- 🔍 Revisar [problemas conocidos](https://github.com/razeone/cybersec-script/issues?q=is%3Aissue)

### 🎓 **Para Uso Institucional**
Si planeas usar esta herramienta en:
- 🏫 Universidades o institutos
- 🏢 Programas de capacitación corporativa  
- 🎯 Talleres de ciberseguridad

¡Nos encantaría saber sobre tu experiencia! Comparte tu feedback para mejorar la herramienta.

---

<div align="center">

### 🌟 **¡Dale una estrella al proyecto si te fue útil!** ⭐

**🛡️ Recuerda: La privacidad es un derecho fundamental**  
*Usa esta herramienta para educar y proteger*

---

[![Cybersecurity](https://img.shields.io/badge/Built%20for-Cybersecurity%20Education-red?style=flat-square&logo=shield)](https://github.com/razeone/cybersec-script)
[![Spanish](https://img.shields.io/badge/Idioma-Español-yellow?style=flat-square)](https://github.com/razeone/cybersec-script)
[![Docker](https://img.shields.io/badge/Deploy%20with-Docker-blue?style=flat-square&logo=docker)](https://github.com/razeone/cybersec-script)

</div>
