# Makefile para Servidor de Análisis de Exposición de Datos
# Versión: 2.0 - Edición Revelada (Español)

# Variables
IMAGE_NAME = cybersec-demo
CONTAINER_NAME = cybersec-demo-es
PORT = 5000
VERSION = latest

# Colores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help build run stop clean logs health test dev prod

# Mostrar ayuda por defecto
help:
	@echo "${GREEN}🕵️ Servidor de Análisis de Exposición de Datos - Docker${NC}"
	@echo "${YELLOW}Comandos disponibles:${NC}"
	@echo "  ${GREEN}build${NC}     - Construir imagen Docker"
	@echo "  ${GREEN}run${NC}       - Ejecutar contenedor"
	@echo "  ${GREEN}stop${NC}      - Detener contenedor"
	@echo "  ${GREEN}restart${NC}   - Reiniciar contenedor"
	@echo "  ${GREEN}logs${NC}      - Ver logs del contenedor"
	@echo "  ${GREEN}health${NC}    - Verificar salud del contenedor"
	@echo "  ${GREEN}clean${NC}     - Limpiar contenedores e imágenes"
	@echo "  ${GREEN}test${NC}      - Probar endpoints"
	@echo "  ${GREEN}dev${NC}       - Ejecutar en modo desarrollo"
	@echo "  ${GREEN}prod${NC}      - Ejecutar en modo producción"
	@echo "  ${GREEN}compose-up${NC}   - Usar Docker Compose"
	@echo "  ${GREEN}compose-down${NC} - Detener Docker Compose"

# Construir imagen Docker
build:
	@echo "${GREEN}🔨 Construyendo imagen Docker...${NC}"
	docker build -t $(IMAGE_NAME):$(VERSION) .
	@echo "${GREEN}✅ Imagen construida: $(IMAGE_NAME):$(VERSION)${NC}"

# Ejecutar contenedor
run: build
	@echo "${GREEN}🚀 Ejecutando contenedor...${NC}"
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):5000 \
		--restart unless-stopped \
		$(IMAGE_NAME):$(VERSION)
	@echo "${GREEN}✅ Contenedor ejecutándose en http://localhost:$(PORT)${NC}"

# Detener contenedor
stop:
	@echo "${YELLOW}⏹️ Deteniendo contenedor...${NC}"
	@docker stop $(CONTAINER_NAME) 2>/dev/null || echo "${RED}Contenedor no está ejecutándose${NC}"

# Reiniciar contenedor
restart: stop run

# Ver logs
logs:
	@echo "${GREEN}📋 Logs del contenedor:${NC}"
	docker logs -f $(CONTAINER_NAME)

# Verificar salud
health:
	@echo "${GREEN}🏥 Verificando salud del contenedor...${NC}"
	@if docker ps | grep -q $(CONTAINER_NAME); then \
		echo "${GREEN}✅ Contenedor ejecutándose${NC}"; \
		curl -f http://localhost:$(PORT)/salud && echo "\n${GREEN}✅ Endpoint de salud OK${NC}" || echo "${RED}❌ Endpoint de salud FALLO${NC}"; \
	else \
		echo "${RED}❌ Contenedor no está ejecutándose${NC}"; \
	fi

# Limpiar contenedores e imágenes
clean:
	@echo "${YELLOW}🧹 Limpiando contenedores e imágenes...${NC}"
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@docker rmi $(IMAGE_NAME):$(VERSION) 2>/dev/null || true
	@docker system prune -f
	@echo "${GREEN}✅ Limpieza completada${NC}"

# Probar endpoints principales
test:
	@echo "${GREEN}🧪 Probando endpoints...${NC}"
	@echo "Probando endpoint de salud..."
	@curl -s http://localhost:$(PORT)/salud | jq . || echo "${RED}❌ /salud falló${NC}"
	@echo "\nProbando endpoint principal..."
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:$(PORT)/ && echo " ${GREEN}✅ / OK${NC}" || echo "${RED}❌ / falló${NC}"
	@echo "\nProbando endpoint de consejos..."
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:$(PORT)/consejos-privacidad && echo " ${GREEN}✅ /consejos-privacidad OK${NC}" || echo "${RED}❌ /consejos-privacidad falló${NC}"

# Modo desarrollo
dev:
	@echo "${GREEN}🔧 Ejecutando en modo desarrollo...${NC}"
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):5000 \
		-e FLASK_ENV=development \
		-e FLASK_DEBUG=1 \
		$(IMAGE_NAME):$(VERSION)
	@echo "${GREEN}✅ Contenedor en modo desarrollo: http://localhost:$(PORT)${NC}"

# Modo producción
prod:
	@echo "${GREEN}🏭 Ejecutando en modo producción...${NC}"
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):5000 \
		-e FLASK_ENV=production \
		-e FLASK_DEBUG=0 \
		--restart unless-stopped \
		$(IMAGE_NAME):$(VERSION)
	@echo "${GREEN}✅ Contenedor en modo producción: http://localhost:$(PORT)${NC}"

# Docker Compose - Iniciar
compose-up:
	@echo "${GREEN}🐳 Iniciando con Docker Compose...${NC}"
	docker-compose up --build -d
	@echo "${GREEN}✅ Servicios iniciados con Docker Compose${NC}"

# Docker Compose - Detener
compose-down:
	@echo "${YELLOW}🐳 Deteniendo Docker Compose...${NC}"
	docker-compose down
	@echo "${GREEN}✅ Servicios detenidos${NC}"

# Información del contenedor
info:
	@echo "${GREEN}📊 Información del contenedor:${NC}"
	@docker ps | grep $(CONTAINER_NAME) || echo "${RED}Contenedor no ejecutándose${NC}"
	@echo "\n${GREEN}📈 Uso de recursos:${NC}"
	@docker stats $(CONTAINER_NAME) --no-stream 2>/dev/null || echo "${RED}Estadísticas no disponibles${NC}"

# Abrir shell en el contenedor
shell:
	@echo "${GREEN}🐚 Abriendo shell en el contenedor...${NC}"
	docker exec -it $(CONTAINER_NAME) /bin/bash

# Mostrar puertos
ports:
	@echo "${GREEN}🔌 Puertos expuestos:${NC}"
	@docker port $(CONTAINER_NAME) 2>/dev/null || echo "${RED}Contenedor no ejecutándose${NC}"
