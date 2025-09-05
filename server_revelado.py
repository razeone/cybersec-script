#!/usr/bin/env python3
"""
🕵️ SERVIDOR DE ANÁLISIS DE EXPOSICIÓN DE DATOS - EDICIÓN REVELADA (ESPAÑOL)
==================================================================================

Un servidor Flask que revela EXACTAMENTE qué datos pueden ver los sitios web sobre ti.
Esta versión incluye explicaciones detalladas en español para educación en ciberseguridad.

Uso: python server_revelado.py
Luego visita: http://localhost:5000

Autor: Asistente de Ciberseguridad
Fecha: 5 de septiembre de 2025
Versión: 2.0 (Revelada - Español)
"""

from flask import Flask, request, jsonify, render_template_string
import hashlib
import json
import requests
from datetime import datetime
from urllib.parse import urlparse
import re
import platform
import socket

app = Flask(__name__)

# Plantilla HTML mejorada en español
PAGINA_DEMO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🕵️ Análisis de Exposición de Datos Personales</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255, 0, 0, 0.2);
            border-radius: 10px;
            border: 2px solid #ff6b6b;
        }
        
        .warning {
            background: rgba(255, 107, 107, 0.3);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #ff6b6b;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 0.8; }
            50% { opacity: 1; }
            100% { opacity: 0.8; }
        }
        
        .scan-button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a5a);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            display: block;
            margin: 20px auto;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
        
        .scan-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 20px rgba(255, 107, 107, 0.6);
        }
        
        .loading {
            text-align: center;
            font-size: 18px;
            color: #4ecdc4;
            display: none;
        }
        
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top: 4px solid #4ecdc4;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .section {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            margin: 15px 0;
            border-radius: 10px;
            border-left: 4px solid #4CAF50;
        }
        
        .section.warning {
            border-left-color: #ff6b6b;
            background: rgba(255, 107, 107, 0.2);
        }
        
        .section.info {
            border-left-color: #2196F3;
            background: rgba(33, 150, 243, 0.2);
        }
        
        .data-item {
            margin: 10px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
        }
        
        .data-label {
            font-weight: bold;
            color: #4ecdc4;
            margin-bottom: 5px;
        }
        
        .data-value {
            color: #ff6b6b;
            font-family: 'Courier New', monospace;
            margin-bottom: 5px;
            word-break: break-all;
        }
        
        .data-explanation {
            font-style: italic;
            color: #ffffff;
            opacity: 0.9;
            font-size: 0.9em;
            line-height: 1.4;
        }
        
        .privacy-score {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .score-high {
            background: rgba(76, 175, 80, 0.3);
            border: 2px solid #4CAF50;
        }
        
        .score-medium {
            background: rgba(255, 193, 7, 0.3);
            border: 2px solid #FFC107;
        }
        
        .score-low {
            background: rgba(255, 107, 107, 0.3);
            border: 2px solid #ff6b6b;
        }
        
        .collapsible {
            cursor: pointer;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            margin: 10px 0;
            transition: background 0.3s ease;
        }
        
        .collapsible:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .collapsible-content {
            display: none;
            padding: 15px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            margin-top: 10px;
        }
        
        .protection-tip {
            margin: 8px 0;
            padding: 12px;
            background: rgba(76, 175, 80, 0.2);
            border-radius: 6px;
            border-left: 3px solid #4CAF50;
        }
        
        .risk-factor {
            margin: 5px 0;
            padding: 8px;
            background: rgba(255, 107, 107, 0.2);
            border-radius: 4px;
            border-left: 3px solid #ff6b6b;
        }
        
        .evaluation-step {
            margin: 10px 0;
            padding: 12px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            border-left: 3px solid #4ecdc4;
        }
        
        .positive-factor {
            background: rgba(76, 175, 80, 0.2);
            border-left-color: #4CAF50;
        }
        
        .negative-factor {
            background: rgba(255, 107, 107, 0.2);
            border-left-color: #ff6b6b;
        }
        
        .calculation-box {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
                margin: 10px;
            }
            
            .header h1 {
                font-size: 1.5em;
            }
            
            .scan-button {
                padding: 12px 25px;
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕵️ ANÁLISIS DE EXPOSICIÓN DE DATOS PERSONALES</h1>
            <p style="margin-top: 10px; font-size: 1.1em;">Descubre EXACTAMENTE qué información pueden ver los sitios web sobre ti</p>
        </div>
        
        <div class="warning">
            <h2>⚠️ ADVERTENCIA DE PRIVACIDAD</h2>
            <p><strong>Este es un demostrador educativo de ciberseguridad.</strong></p>
            <p>Los sitios web reales pueden recopilar TODA esta información (y más) sin tu conocimiento o consentimiento explícito. Esta herramienta te muestra lo vulnerable que está tu privacidad en línea.</p>
            <p><strong>¡PROTÉGETE!</strong> Usa esta información para mejorar tu privacidad digital.</p>
        </div>
        
        <div style="text-align: center;">
            <button class="scan-button" onclick="iniciarEscaneo()">
                🔍 ESCANEAR MI EXPOSICIÓN DE DATOS
            </button>
            
            <div style="margin: 20px 0; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
                <button onclick="establecerCookiesDemo()" style="background: #FFC107; color: #000; border: none; padding: 10px 15px; border-radius: 15px; cursor: pointer; font-weight: bold;">
                    🍪 Establecer Cookies de Prueba
                </button>
                <button onclick="limpiarCookies()" style="background: #f44336; color: white; border: none; padding: 10px 15px; border-radius: 15px; cursor: pointer; font-weight: bold;">
                    🗑️ Limpiar Cookies
                </button>
                <button onclick="probarConfiguracion()" style="background: #4CAF50; color: white; border: none; padding: 10px 15px; border-radius: 15px; cursor: pointer; font-weight: bold;">
                    ⚙️ Probar Mi Configuración
                </button>
                <button onclick="verConsejosPrivacidad()" style="background: #2196F3; color: white; border: none; padding: 10px 15px; border-radius: 15px; cursor: pointer; font-weight: bold;">
                    💡 Consejos de Privacidad
                </button>
            </div>
        </div>
        
        <div class="loading" id="cargando">
            <div class="spinner"></div>
            <p>Analizando tu huella digital...</p>
            <p>Recopilando datos de tu navegador...</p>
            <p>Evaluando riesgos de privacidad...</p>
        </div>
        
        <div id="resultados" class="results" style="display: none;"></div>
    </div>

    <script>
        async function iniciarEscaneo() {
            document.getElementById('cargando').style.display = 'block';
            document.getElementById('resultados').style.display = 'none';
            
            // Simular tiempo de carga realista
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Recopilar datos del lado del cliente
            const datosCliente = recopilarDatosCliente();
            
            try {
                const respuesta = await fetch('/analizar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(datosCliente)
                });
                
                const datos = await respuesta.json();
                mostrarResultadosExplicados(datos);
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('resultados').innerHTML = 
                    '<div style="color: #ff6b6b; text-align: center;">Error al analizar los datos. Intenta de nuevo.</div>';
            }
            
            document.getElementById('cargando').style.display = 'none';
            document.getElementById('resultados').style.display = 'block';
        }
        
        function recopilarDatosCliente() {
            // Recopilar información del navegador y dispositivo
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillText('Huella digital de canvas 🔍', 2, 2);
            const huellaCanvas = canvas.toDataURL().substring(0, 50);
            
            // Información WebGL
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            const huellaWebGL = gl ? 
                gl.getParameter(gl.VENDOR) + ' - ' + gl.getParameter(gl.RENDERER) : 
                'WebGL no disponible';
            
            // Información del navegador
            const infoNavegador = {
                idioma: navigator.language,
                idiomas: navigator.languages || [navigator.language],
                plataforma: navigator.platform,
                fabricante: navigator.vendor || 'Desconocido',
                cookiesHabilitadas: navigator.cookieEnabled,
                noRastrear: navigator.doNotTrack,
                concurrenciaHardware: navigator.hardwareConcurrency || 'Desconocido',
                puntosToqueMaximos: navigator.maxTouchPoints || 0,
                enLinea: navigator.onLine
            };
            
            // Información de almacenamiento
            let infoAlmacenamiento = {
                localStorage: false,
                sessionStorage: false,
                datosLocalStorage: {},
                datosSessionStorage: {}
            };
            
            try {
                infoAlmacenamiento.localStorage = typeof(Storage) !== "undefined" && localStorage;
                infoAlmacenamiento.sessionStorage = typeof(Storage) !== "undefined" && sessionStorage;
                
                if (infoAlmacenamiento.localStorage) {
                    for (let i = 0; i < localStorage.length; i++) {
                        const clave = localStorage.key(i);
                        infoAlmacenamiento.datosLocalStorage[clave] = localStorage.getItem(clave).substring(0, 100);
                    }
                }
                
                if (infoAlmacenamiento.sessionStorage) {
                    for (let i = 0; i < sessionStorage.length; i++) {
                        const clave = sessionStorage.key(i);
                        infoAlmacenamiento.datosSessionStorage[clave] = sessionStorage.getItem(clave).substring(0, 100);
                    }
                }
            } catch (e) {
                console.log('Error accediendo al almacenamiento:', e);
            }
            
            // Información de plugins
            const plugins = [];
            for (let i = 0; i < navigator.plugins.length; i++) {
                plugins.push({
                    nombre: navigator.plugins[i].name,
                    descripcion: navigator.plugins[i].description
                });
            }
            
            return {
                huella_canvas: huellaCanvas,
                huella_webgl: huellaWebGL,
                ancho_pantalla: screen.width,
                alto_pantalla: screen.height,
                profundidad_color_pantalla: screen.colorDepth,
                relacion_pixeles_dispositivo: window.devicePixelRatio || 1,
                zona_horaria: Intl.DateTimeFormat().resolvedOptions().timeZone,
                java_habilitado: typeof java !== 'undefined',
                configuracion_regional: Intl.DateTimeFormat().resolvedOptions().locale,
                info_navegador: infoNavegador,
                plugins: plugins,
                info_almacenamiento: infoAlmacenamiento,
                alto_ventana: window.innerHeight,
                ancho_ventana: window.innerWidth,
                cookies: obtenerTodasLasCookies()
            };
        }
        
        function obtenerTodasLasCookies() {
            const cookies = {};
            if (document.cookie) {
                document.cookie.split(';').forEach(cookie => {
                    const [nombre, valor] = cookie.trim().split('=');
                    if (nombre && valor) {
                        cookies[nombre] = valor;
                    }
                });
            }
            return cookies;
        }
        
        function mostrarResultadosExplicados(datos) {
            const divResultados = document.getElementById('resultados');
            
            let html = '<div style="color: #ff6b6b; text-align: center; margin-bottom: 20px; font-size: 1.2em; font-weight: bold;">' +
                      '🚨 ESTO ES LO QUE LOS SITIOS WEB PUEDEN VER SOBRE TI 🚨' +
                      '</div>';
            
            // Puntuación de privacidad con explicación detallada
            const puntuacion = datos.puntuacion_privacidad || 50;
            const clasesPuntuacion = puntuacion > 70 ? 'score-high' : puntuacion > 40 ? 'score-medium' : 'score-low';
            const textoPuntuacion = puntuacion > 70 ? 'BUENA PRIVACIDAD' : puntuacion > 40 ? 'PRIVACIDAD MODERADA' : 'PRIVACIDAD DEFICIENTE';
            
            html += '<div class="privacy-score ' + clasesPuntuacion + '">' +
                   '🛡️ Tu Puntuación de Privacidad: ' + puntuacion + '/100 (' + textoPuntuacion + ')' +
                   '</div>';
            html += '<div style="font-style: italic; margin-bottom: 20px; text-align: center;">' + datos.explicacion_puntuacion + '</div>';
            
            // Mostrar evaluación detallada
            if (datos.evaluacion_detallada) {
                html += '<div style="text-align: center; margin: 20px 0;">';
                html += '<button onclick="alternarEvaluacionDetallada()" style="background: #4ecdc4; color: #000; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer; font-weight: bold;">';
                html += '📊 Ver Evaluación Detallada y Cómo Mejorar';
                html += '</button>';
                html += '</div>';
                html += '<div id="evaluacionDetallada" style="display: none;">';
                html += mostrarEvaluacionDetallada(datos.evaluacion_detallada);
                html += '</div>';
            }
            
            // Sección de Ubicación y Red
            html += crearSeccionExplicada('📍 Tu Ubicación y Conexión a Internet', [
                {
                    etiqueta: 'Tu Dirección de Internet (IP)',
                    valor: datos.direccion_ip,
                    explicacion: datos.explicacion_ip
                },
                {
                    etiqueta: 'Tu Ubicación Aproximada',
                    valor: datos.ubicacion,
                    explicacion: datos.explicacion_ubicacion
                },
                {
                    etiqueta: 'Tu Proveedor de Internet',
                    valor: datos.isp,
                    explicacion: datos.explicacion_isp
                },
                {
                    etiqueta: 'Tipo de Conexión',
                    valor: datos.tipo_conexion,
                    explicacion: datos.explicacion_conexion
                }
            ]);
            
            // Sección de Dispositivo y Navegador
            html += crearSeccionExplicada('💻 Tu Dispositivo y Navegador', [
                {
                    etiqueta: 'Sistema Operativo',
                    valor: datos.info_so,
                    explicacion: datos.explicacion_so
                },
                {
                    etiqueta: 'Navegador Web',
                    valor: datos.navegador,
                    explicacion: datos.explicacion_navegador
                },
                {
                    etiqueta: 'Resolución de Pantalla',
                    valor: datos.info_pantalla,
                    explicacion: datos.explicacion_pantalla
                },
                {
                    etiqueta: 'Zona Horaria',
                    valor: datos.zona_horaria,
                    explicacion: datos.explicacion_zona_horaria
                },
                {
                    etiqueta: 'Preferencia de Idioma',
                    valor: datos.idioma,
                    explicacion: datos.explicacion_idioma
                }
            ]);
            
            // Sección de Huella Digital del Navegador (Mejorada)
            html += crearSeccionHuellaDigital(datos);
            
            // Sección de Seguimiento y Privacidad
            html += crearSeccionExplicada('🕵️ Información de Seguimiento y Privacidad', [
                {
                    etiqueta: 'Cookies en Tu Dispositivo',
                    valor: datos.contador_cookies + ' cookies encontradas',
                    explicacion: datos.explicacion_cookies
                },
                {
                    etiqueta: 'Cookies de Seguimiento',
                    valor: datos.tiene_cookies_seguimiento ? 'SÍ - ¡Estás siendo rastreado!' : 'Ninguna detectada',
                    explicacion: datos.explicacion_seguimiento
                },
                {
                    etiqueta: 'Configuración No Rastrear',
                    valor: datos.no_rastrear,
                    explicacion: datos.explicacion_nrt
                },
                {
                    etiqueta: 'ID de Sesión',
                    valor: datos.id_sesion,
                    explicacion: datos.explicacion_sesion
                }
            ]);
            
            // Sección de Riesgos de Privacidad
            if (datos.riesgo_seguimiento && datos.riesgo_seguimiento.factores) {
                html += '<div class="section warning">';
                html += '<h3>⚠️ Riesgos de Privacidad Detectados</h3>';
                html += '<div style="font-style: italic; margin-bottom: 10px;">' + datos.explicacion_riesgo + '</div>';
                html += '<div><strong>Nivel de Riesgo:</strong> ' + datos.riesgo_seguimiento.nivel + '</div>';
                html += '<div style="margin-top: 10px;"><strong>Riesgos Específicos:</strong></div>';
                datos.riesgo_seguimiento.factores.forEach(factor => {
                    html += '<div class="risk-factor">• ' + factor + '</div>';
                });
                html += '</div>';
            }
            
            // Consejos de Protección
            html += '<div class="section" style="border-left-color: #4CAF50;">';
            html += '<h3>🛡️ Cómo Proteger Tu Privacidad</h3>';
            html += '<div class="protection-tip">';
            html += '<strong>🔒 Usa una VPN:</strong> Oculta tu dirección IP real y ubicación de sitios web y anunciantes';
            html += '</div>';
            html += '<div class="protection-tip">';
            html += '<strong>🕵️ Navegación Privada:</strong> Usa modo incógnito/privado para reducir el seguimiento entre sesiones';
            html += '</div>';
            html += '<div class="protection-tip">';
            html += '<strong>🚫 Bloqueadores de Anuncios:</strong> Instala uBlock Origin para bloquear rastreadores y anuncios maliciosos';
            html += '</div>';
            html += '<div class="protection-tip">';
            html += '<strong>🗑️ Limpiar Datos:</strong> Elimina regularmente cookies y datos de navegación';
            html += '</div>';
            html += '<div class="protection-tip">';
            html += '<strong>🛡️ Navegadores Seguros:</strong> Considera usar Firefox con configuración endurecida o Tor Browser';
            html += '</div>';
            html += '</div>';
            
            // Protección Específica contra Huellas Digitales
            html += '<div class="section info">';
            html += '<h3>🔍 Protección Específica contra Huellas Digitales</h3>';
            html += '<div class="protection-tip">';
            html += '<strong>🎭 Extensiones Anti-Huella:</strong> Instala extensiones como Canvas Blocker o ClearURLs para falsificar o bloquear huellas digitales';
            html += '</div>';
            html += '<div class="protection-tip">';
            html += '<strong>🔄 Cambiar User-Agent:</strong> Usa extensiones que rotan tu user-agent para confundir a los rastreadores';
            html += '</div>';
            html += '<div class="protection-tip">';
            html += '<strong>📱 Configuración del Navegador:</strong> Desactiva JavaScript en sitios no confiables y ajusta la configuración de privacidad';
            html += '</div>';
            html += '<div class="protection-tip">';
            html += '<strong>🎯 Resistencia de Huella Firefox:</strong> Activa "privacy.resistFingerprinting" en about:config';
            html += '</div>';
            html += '</div>';
            
            // Datos Técnicos (Colapsables)
            if (datos.datos_tecnicos) {
                html += '<div class="collapsible" onclick="alternarContenidoColapsable(this)">';
                html += '<h3>🔧 Datos Técnicos Completos (Clic para expandir)</h3>';
                html += '</div>';
                html += '<div class="collapsible-content">';
                html += '<pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 0.8em;">';
                html += JSON.stringify(datos.datos_tecnicos, null, 2);
                html += '</pre>';
                html += '</div>';
            }
            
            divResultados.innerHTML = html;
        }
        
        function crearSeccionExplicada(titulo, elementos) {
            let html = '<div class="section">';
            html += '<h3>' + titulo + '</h3>';
            
            elementos.forEach(elemento => {
                html += '<div class="data-item">';
                html += '<div class="data-label">' + elemento.etiqueta + ':</div>';
                html += '<div class="data-value">' + elemento.valor + '</div>';
                html += '<div class="data-explanation">' + elemento.explicacion + '</div>';
                html += '</div>';
            });
            
            html += '</div>';
            return html;
        }
        
        function crearSeccionHuellaDigital(datos) {
            let html = '<div class="section warning">';
            html += '<h3>🔍 Huella Digital de Tu Navegador (Información Crítica)</h3>';
            html += '<div style="font-style: italic; margin-bottom: 15px;">';
            html += 'Tu huella digital del navegador es como una "firma" única que se crea combinando características de tu dispositivo y navegador. ';
            html += 'Esta información puede ser usada para rastrearte incluso sin cookies.';
            html += '</div>';
            
            const elementosHuella = [
                {
                    etiqueta: 'Huella Única del Navegador',
                    valor: datos.huella_unica,
                    explicacion: datos.explicacion_huella
                },
                {
                    etiqueta: 'Huella Canvas',
                    valor: datos.huella_canvas || 'No disponible',
                    explicacion: datos.explicacion_canvas
                },
                {
                    etiqueta: 'Huella WebGL',
                    valor: datos.huella_webgl || 'No disponible',
                    explicacion: datos.explicacion_webgl
                },
                {
                    etiqueta: 'Información de Hardware',
                    valor: datos.info_hardware || 'No disponible',
                    explicacion: datos.explicacion_hardware
                },
                {
                    etiqueta: 'Plugins Instalados',
                    valor: datos.plugins ? datos.plugins.length + ' plugins detectados' : 'No disponible',
                    explicacion: datos.explicacion_plugins
                }
            ];
            
            elementosHuella.forEach(elemento => {
                if (elemento.valor && elemento.valor !== 'No disponible') {
                    html += '<div class="data-item">';
                    html += '<div class="data-label">' + elemento.etiqueta + ':</div>';
                    html += '<div class="data-value">' + elemento.valor + '</div>';
                    html += '<div class="data-explanation">' + elemento.explicacion + '</div>';
                    html += '</div>';
                }
            });
            
            // Resistencia de Huella Digital
            if (datos.resistencia_huella) {
                html += '<div style="margin-top: 15px; padding: 10px; background: rgba(255,193,7,0.2); border-radius: 5px; border-left: 3px solid #FFC107;">';
                html += '<div class="data-label">Resistencia a Huellas Digitales:</div>';
                html += '<div class="data-value">' + datos.resistencia_huella.nivel + '</div>';
                html += '<div class="data-explanation">' + datos.resistencia_huella.explicacion + '</div>';
                if (datos.resistencia_huella.recomendaciones) {
                    html += '<div style="margin-top: 10px;"><strong>Recomendaciones:</strong></div>';
                    datos.resistencia_huella.recomendaciones.forEach(rec => {
                        html += '<div style="margin: 5px 0; padding: 5px; background: rgba(255,255,255,0.1); border-radius: 3px;">• ' + rec + '</div>';
                    });
                }
                html += '</div>';
            }
            
            html += '</div>';
            return html;
        }
        
        function mostrarEvaluacionDetallada(evaluacion) {
            let html = '<div class="section info">';
            html += '<h3>📊 Evaluación Detallada de Privacidad</h3>';
            html += '<div style="margin-bottom: 15px; font-style: italic;">';
            html += 'Tu puntuación se calculó evaluando los siguientes factores. Cada factor tiene un impacto específico en tu privacidad:';
            html += '</div>';
            
            // Mostrar cálculo paso a paso
            html += '<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 15px 0;">';
            html += '<h4>🧮 Cálculo de Puntuación:</h4>';
            html += '<div style="margin: 10px 0; font-family: monospace;">';
            html += '<span style="color: #4ecdc4;">Puntuación inicial:</span> <span style="color: #ffffff;">' + evaluacion.puntuacion_inicial + ' puntos</span>';
            html += '</div>';
            
            // Factores negativos
            if (evaluacion.detalles_evaluacion && evaluacion.detalles_evaluacion.length > 0) {
                html += '<div style="margin-top: 15px;"><h4>⚠️ Factores que Reducen tu Privacidad:</h4>';
                evaluacion.detalles_evaluacion.forEach(factor => {
                    html += '<div style="background: rgba(255,107,107,0.2); margin: 8px 0; padding: 12px; border-radius: 6px; border-left: 3px solid #ff6b6b;">';
                    html += '<div style="font-weight: bold; color: #ff6b6b; margin-bottom: 5px;">' + factor.factor + ' ' + factor.impacto + '</div>';
                    html += '<div style="margin-bottom: 8px; font-size: 0.9em;">' + factor.explicacion + '</div>';
                    html += '<div style="font-weight: bold; color: #4ecdc4;">💡 Cómo mejorar:</div>';
                    html += '<div style="font-style: italic; color: #ffffff;">' + factor.mejora + '</div>';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            // Factores positivos
            if (evaluacion.factores_positivos && evaluacion.factores_positivos.length > 0) {
                html += '<div style="margin-top: 15px;"><h4>✅ Factores Positivos:</h4>';
                evaluacion.factores_positivos.forEach(factor => {
                    html += '<div style="background: rgba(76,175,80,0.2); margin: 8px 0; padding: 12px; border-radius: 6px; border-left: 3px solid #4CAF50;">';
                    html += '<div style="font-weight: bold; color: #4CAF50; margin-bottom: 5px;">' + factor.factor + ' ' + factor.beneficio + '</div>';
                    html += '<div style="font-size: 0.9em;">' + factor.explicacion + '</div>';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            // Puntuación final
            html += '<div style="margin-top: 15px; text-align: center; font-size: 1.2em;">';
            html += '<span style="color: #4ecdc4;">Puntuación final:</span> ';
            html += '<span style="color: #ffffff; font-weight: bold; font-size: 1.3em;">' + evaluacion.puntuacion + '/100</span>';
            html += '<span style="color: #ffffff;"> (' + evaluacion.nivel + ')</span>';
            html += '</div>';
            
            // Recomendaciones principales
            if (evaluacion.recomendaciones_mejora && evaluacion.recomendaciones_mejora.length > 0) {
                html += '<div style="margin-top: 20px; background: rgba(255,193,7,0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #FFC107;">';
                html += '<h4>🚀 Acciones Inmediatas para Mejorar:</h4>';
                evaluacion.recomendaciones_mejora.forEach(recomendacion => {
                    html += '<div style="margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">';
                    html += recomendacion;
                    html += '</div>';
                });
                html += '</div>';
            }
            
            html += '</div>';
            html += '</div>';
            
            return html;
        }
        
        function alternarContenidoColapsable(elemento) {
            const contenido = elemento.nextElementSibling;
            if (contenido.style.display === 'none' || contenido.style.display === '') {
                contenido.style.display = 'block';
            } else {
                contenido.style.display = 'none';
            }
        }
        
        function alternarEvaluacionDetallada() {
            const evaluacion = document.getElementById('evaluacionDetallada');
            const boton = event.target;
            
            if (evaluacion.style.display === 'none' || evaluacion.style.display === '') {
                evaluacion.style.display = 'block';
                boton.textContent = '📊 Ocultar Evaluación Detallada';
                boton.style.background = '#ff6b6b';
                boton.style.color = '#fff';
            } else {
                evaluacion.style.display = 'none';
                boton.textContent = '📊 Ver Evaluación Detallada y Cómo Mejorar';
                boton.style.background = '#4ecdc4';
                boton.style.color = '#000';
            }
        }
        
        async function establecerCookiesDemo() {
            try {
                const respuesta = await fetch('/establecer-cookies-demo');
                const datos = await respuesta.json();
                alert('✅ ' + datos.mensaje + '\\n\\nCookies creadas: ' + datos.cookies_creadas.join(', ') + '\\n\\n🔄 Haz clic en "Escanear" para ver el cambio');
            } catch (error) {
                alert('❌ Error al establecer cookies de demostración');
            }
        }
        
        async function limpiarCookies() {
            try {
                const respuesta = await fetch('/limpiar-cookies');
                const datos = await respuesta.json();
                alert('🗑️ ' + datos.mensaje + '\\n\\n🔄 Haz clic en "Escanear" para ver el cambio');
                // Recargar la página para reflejar los cambios
                setTimeout(() => window.location.reload(), 1000);
            } catch (error) {
                alert('❌ Error al limpiar cookies');
            }
        }
        
        async function probarConfiguracion() {
            try {
                const respuesta = await fetch('/prueba-configuracion');
                const datos = await respuesta.json();
                
                let mensaje = `🛡️ PRUEBA DE CONFIGURACIÓN DE PRIVACIDAD\\n`;
                mensaje += `Puntuación: ${datos.puntuacion_total}/${datos.puntuacion_maxima}\\n`;
                mensaje += `Nivel: ${datos.nivel_general}\\n\\n`;
                mensaje += `${datos.mensaje}\\n\\n`;
                mensaje += `RESULTADOS DETALLADOS:\\n`;
                
                Object.entries(datos.pruebas).forEach(([nombre, resultado]) => {
                    mensaje += `• ${resultado.descripcion} (${resultado.puntos} puntos)\\n`;
                });
                
                alert(mensaje);
            } catch (error) {
                alert('❌ Error al probar configuración');
            }
        }
        
        async function verConsejosPrivacidad() {
            try {
                const respuesta = await fetch('/consejos-privacidad');
                const datos = await respuesta.json();
                
                // Crear contenido HTML con los consejos reales
                let contenidoConsejos = `
                    <html>
                    <head>
                        <title>Consejos de Privacidad Digital</title>
                        <style>
                            body { 
                                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                                margin: 20px; 
                                line-height: 1.6; 
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: #333;
                            }
                            .container {
                                max-width: 800px;
                                margin: 0 auto;
                                background: white;
                                padding: 30px;
                                border-radius: 15px;
                                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                            }
                            h1, h2, h3 { color: #333; margin-top: 0; }
                            h1 { text-align: center; color: #764ba2; }
                            .seccion { margin: 20px 0; }
                            .consejo { 
                                background: #f8f9ff; 
                                padding: 15px; 
                                margin: 10px 0; 
                                border-radius: 8px; 
                                border-left: 4px solid #667eea;
                            }
                            .consejo h4 { margin: 0 0 8px 0; color: #667eea; }
                            .navegador-item, .extension-item, .vpn-item { 
                                background: #e8f5e8; 
                                padding: 12px; 
                                margin: 8px 0; 
                                border-radius: 6px; 
                                border-left: 4px solid #4CAF50;
                            }
                            .habito-item { 
                                background: #fff3e0; 
                                padding: 10px; 
                                margin: 8px 0; 
                                border-radius: 6px; 
                                border-left: 4px solid #FF9800;
                            }
                            .nivel { 
                                background: #764ba2; 
                                color: white; 
                                padding: 4px 8px; 
                                border-radius: 4px; 
                                font-size: 0.8em; 
                                font-weight: bold;
                                display: inline-block;
                                margin-top: 8px;
                            }
                            .herramienta { 
                                background: #e8f5e8; 
                                padding: 12px; 
                                margin: 8px 0; 
                                border-radius: 6px; 
                                border-left: 4px solid #4CAF50;
                            }
                            .config { 
                                background: #fff3e0; 
                                padding: 10px; 
                                margin: 8px 0; 
                                border-radius: 6px; 
                                border-left: 4px solid #FF9800;
                            }
                            .navegador { margin: 15px 0; }
                            .navegador h4 { color: #FF9800; margin-bottom: 10px; }
                            .config-item { margin: 5px 0 5px 20px; }
                            .close-btn {
                                background: #764ba2;
                                color: white;
                                border: none;
                                padding: 12px 24px;
                                border-radius: 6px;
                                cursor: pointer;
                                font-size: 16px;
                                margin: 20px auto;
                                display: block;
                            }
                            .close-btn:hover { background: #5a3a7a; }
                            .pasos { margin-top: 10px; }
                            .pasos ul { margin: 5px 0; padding-left: 20px; }
                            .pasos li { margin: 3px 0; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>�️ Guía Completa de Privacidad Digital</h1>
                            <p style="text-align: center; font-style: italic; color: #666;">
                                <strong>Actualizada:</strong> ${new Date().toLocaleDateString('es-ES')}
                            </p>
                `;
                
                // Agregar navegadores seguros
                if (datos.consejos && datos.consejos.navegadores_seguros) {
                    contenidoConsejos += `
                        <div class="seccion">
                            <h2>🌐 Navegadores Seguros Recomendados</h2>
                    `;
                    datos.consejos.navegadores_seguros.forEach(navegador => {
                        contenidoConsejos += `
                            <div class="navegador-item">
                                <h4>${navegador.nombre}</h4>
                                <p>${navegador.descripcion}</p>
                                <div class="nivel">Nivel: ${navegador.nivel}</div>
                                ${navegador.pasos ? `
                                    <div class="pasos">
                                        <strong>Pasos de configuración:</strong>
                                        <ul>
                                            ${navegador.pasos.map(paso => `<li>${paso}</li>`).join('')}
                                        </ul>
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    });
                    contenidoConsejos += `</div>`;
                }
                
                // Agregar extensiones de privacidad
                if (datos.consejos && datos.consejos.extensiones_privacidad) {
                    contenidoConsejos += `
                        <div class="seccion">
                            <h2>🧩 Extensiones de Privacidad Esenciales</h2>
                    `;
                    datos.consejos.extensiones_privacidad.forEach(extension => {
                        contenidoConsejos += `
                            <div class="extension-item">
                                <h4>${extension.nombre}</h4>
                                <p><strong>Propósito:</strong> ${extension.proposito}</p>
                                <p><strong>Instalación:</strong> ${extension.instalacion}</p>
                            </div>
                        `;
                    });
                    contenidoConsejos += `</div>`;
                }
                
                // Agregar VPNs recomendadas
                if (datos.consejos && datos.consejos.vpn_recomendadas) {
                    contenidoConsejos += `
                        <div class="seccion">
                            <h2>� VPNs Recomendadas</h2>
                    `;
                    datos.consejos.vpn_recomendadas.forEach(categoria => {
                        contenidoConsejos += `
                            <div class="vpn-item">
                                <h4>${categoria.categoria}</h4>
                                <p><strong>Opciones:</strong> ${categoria.opciones.join(', ')}</p>
                                <p><strong>Características:</strong> ${categoria.caracteristicas.join(', ')}</p>
                            </div>
                        `;
                    });
                    contenidoConsejos += `</div>`;
                }
                
                // Agregar configuraciones de dispositivo
                if (datos.consejos && datos.consejos.configuraciones_dispositivo) {
                    contenidoConsejos += `
                        <div class="seccion">
                            <h2>⚙️ Configuraciones de Dispositivo</h2>
                    `;
                    
                    Object.keys(datos.consejos.configuraciones_dispositivo).forEach(dispositivo => {
                        contenidoConsejos += `
                            <div class="consejo">
                                <h4>${dispositivo.charAt(0).toUpperCase() + dispositivo.slice(1)}</h4>
                                <ul>
                                    ${datos.consejos.configuraciones_dispositivo[dispositivo].map(config => `<li>${config}</li>`).join('')}
                                </ul>
                            </div>
                        `;
                    });
                    contenidoConsejos += `</div>`;
                }
                
                // Agregar hábitos seguros
                if (datos.consejos && datos.consejos.habitos_seguros) {
                    contenidoConsejos += `
                        <div class="seccion">
                            <h2>✅ Hábitos de Seguridad Digital</h2>
                    `;
                    datos.consejos.habitos_seguros.forEach(habito => {
                        contenidoConsejos += `
                            <div class="habito-item">
                                ${habito}
                            </div>
                        `;
                    });
                    contenidoConsejos += `</div>`;
                }
                
                // Cerrar HTML
                contenidoConsejos += `
                            <p style="text-align: center; margin-top: 30px; padding: 20px; background: #f0f0f0; border-radius: 8px;">
                                <strong>💡 Recuerda:</strong> La privacidad es un proceso continuo, no un destino. 
                                Implementa estos consejos gradualmente y mantente actualizado sobre nuevas amenazas y soluciones.
                            </p>
                            <button class="close-btn" onclick="window.close()">🔒 Cerrar Guía</button>
                        </div>
                    </body>
                    </html>
                `;
                
                // Crear nueva ventana con los consejos
                const ventanaConsejos = window.open('', '_blank', 'width=900,height=700,scrollbars=yes,resizable=yes');
                ventanaConsejos.document.write(contenidoConsejos);
                ventanaConsejos.document.close();
                
            } catch (error) {
                console.error('Error cargando consejos:', error);
                alert('❌ Error al cargar consejos de privacidad. Verifica tu conexión e intenta de nuevo.');
            }
        }
    </script>
</body>
</html>
'''

def obtener_ubicacion_ip(ip):
    """Obtener información de ubicación basada en IP"""
    if ip.startswith(('127.', '192.168.', '10.', '172.')):
        return {
            'ciudad': 'Red Local',
            'region': 'IP Privada', 
            'pais': 'Local',
            'isp': 'Red Local',
            'precision': 'N/A - IP Privada'
        }
    
    try:
        # Usar un servicio gratuito de geolocalización IP
        respuesta = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            return {
                'ciudad': datos.get('city', 'Desconocido'),
                'region': datos.get('regionName', 'Desconocido'),
                'pais': datos.get('country', 'Desconocido'),
                'isp': datos.get('isp', 'Desconocido'),
                'precision': f"±{datos.get('accuracy', 'Desconocido')}km"
            }
    except:
        pass
    
    return {
        'ciudad': 'Desconocido',
        'region': 'Desconocido', 
        'pais': 'Desconocido',
        'isp': 'Desconocido',
        'precision': 'No disponible'
    }

def analizar_user_agent(user_agent):
    """Analizar el user agent para extraer información del SO y navegador"""
    so_info = 'Desconocido'
    info_navegador = 'Desconocido'
    
    if user_agent:
        user_agent_lower = user_agent.lower()
        
        # Detectar Sistema Operativo
        if 'windows nt 10' in user_agent_lower:
            so_info = 'Windows 10/11'
        elif 'windows nt 6.3' in user_agent_lower:
            so_info = 'Windows 8.1'
        elif 'windows nt 6.1' in user_agent_lower:
            so_info = 'Windows 7'
        elif 'mac os x' in user_agent_lower or 'macos' in user_agent_lower:
            so_info = 'macOS'
        elif 'iphone' in user_agent_lower:
            so_info = 'iOS (iPhone)'
        elif 'ipad' in user_agent_lower:
            so_info = 'iOS (iPad)'
        elif 'android' in user_agent_lower:
            so_info = 'Android'
        elif 'linux' in user_agent_lower:
            so_info = 'Linux'
        
        # Detectar Navegador
        if 'edg/' in user_agent_lower:
            info_navegador = 'Microsoft Edge'
        elif 'chrome/' in user_agent_lower and 'edg/' not in user_agent_lower:
            info_navegador = 'Google Chrome'
        elif 'firefox/' in user_agent_lower:
            info_navegador = 'Mozilla Firefox'
        elif 'safari/' in user_agent_lower and 'chrome/' not in user_agent_lower:
            info_navegador = 'Safari'
        elif 'opera/' in user_agent_lower or 'opr/' in user_agent_lower:
            info_navegador = 'Opera'
    
    return so_info, info_navegador

def calcular_puntuacion_privacidad(request):
    """Calcular una puntuación de privacidad detallada basada en varios factores"""
    puntuacion_inicial = 100
    puntuacion_actual = puntuacion_inicial
    detalles_evaluacion = []
    factores_positivos = []
    recomendaciones_mejora = []
    
    # Evaluar cookies
    num_cookies = len(request.cookies) if request.cookies else 0
    if num_cookies > 10:
        reduccion = 30
        puntuacion_actual -= reduccion
        detalles_evaluacion.append({
            'factor': f'Muchas cookies detectadas ({num_cookies} cookies)',
            'impacto': f'-{reduccion} puntos',
            'explicacion': 'Tener muchas cookies facilita el seguimiento entre sitios web',
            'mejora': 'Elimina cookies regularmente y usa modo privado'
        })
        recomendaciones_mejora.append('🍪 Limpiar cookies: Ve a Configuración > Privacidad > Borrar datos de navegación')
    elif num_cookies > 5:
        reduccion = 20
        puntuacion_actual -= reduccion
        detalles_evaluacion.append({
            'factor': f'Varias cookies detectadas ({num_cookies} cookies)',
            'impacto': f'-{reduccion} puntos',
            'explicacion': 'Las cookies pueden ser usadas para rastrearte',
            'mejora': 'Configura tu navegador para bloquear cookies de terceros'
        })
        recomendaciones_mejora.append('🔒 Bloquear cookies de terceros en la configuración del navegador')
    elif num_cookies > 0:
        reduccion = 10
        puntuacion_actual -= reduccion
        detalles_evaluacion.append({
            'factor': f'Algunas cookies detectadas ({num_cookies} cookies)',
            'impacto': f'-{reduccion} puntos',
            'explicacion': 'Pocas cookies es aceptable para funcionalidad básica',
            'mejora': 'Monitorea qué cookies aceptas'
        })
    else:
        factores_positivos.append({
            'factor': 'Sin cookies detectadas',
            'beneficio': '+0 puntos (excelente)',
            'explicacion': 'No hay cookies que puedan rastrearte'
        })
    
    # Evaluar header Referer
    if request.headers.get('Referer'):
        reduccion = 15
        puntuacion_actual -= reduccion
        detalles_evaluacion.append({
            'factor': 'Header Referer presente',
            'impacto': f'-{reduccion} puntos',
            'explicacion': 'El header Referer revela desde qué sitio viniste',
            'mejora': 'Configura tu navegador para no enviar referrer'
        })
        recomendaciones_mejora.append('🔗 Configurar referrer policy: Usar extensiones como uBlock Origin')
    else:
        factores_positivos.append({
            'factor': 'Sin header Referer',
            'beneficio': '+0 puntos (bueno)',
            'explicacion': 'Tu historial de navegación no se revela'
        })
    
    # Evaluar Do Not Track
    if not request.headers.get('DNT'):
        reduccion = 10
        puntuacion_actual -= reduccion
        detalles_evaluacion.append({
            'factor': 'Do Not Track no configurado',
            'impacto': f'-{reduccion} puntos',
            'explicacion': 'No estás pidiendo explícitamente no ser rastreado',
            'mejora': 'Activa la opción "Do Not Track" en tu navegador'
        })
        recomendaciones_mejora.append('🚫 Activar Do Not Track: Configuración > Privacidad > Solicitar que no me rastreen')
    else:
        factores_positivos.append({
            'factor': 'Do Not Track activado',
            'beneficio': '+0 puntos (excelente)',
            'explicacion': 'Estás pidiendo no ser rastreado (aunque no siempre se respeta)'
        })
    
    # Evaluar conexión segura
    if not request.is_secure:
        reduccion = 15
        puntuacion_actual -= reduccion
        detalles_evaluacion.append({
            'factor': 'Conexión HTTP (no segura)',
            'impacto': f'-{reduccion} puntos',
            'explicacion': 'Las conexiones HTTP pueden ser interceptadas',
            'mejora': 'Siempre usa HTTPS y habilita "HTTPS-Only mode"'
        })
        recomendaciones_mejora.append('🔒 Usar solo HTTPS: Instalar extensión "HTTPS Everywhere"')
    else:
        factores_positivos.append({
            'factor': 'Conexión HTTPS segura',
            'beneficio': '+0 puntos (excelente)',
            'explicacion': 'Tu conexión está cifrada'
        })
    
    # Evaluar headers de fingerprinting
    headers_fingerprinting = {
        'Sec-Ch-Ua': 'Información del navegador',
        'Sec-Ch-Ua-Platform': 'Información de la plataforma',
        'Sec-Ch-Ua-Mobile': 'Información si es móvil'
    }
    
    headers_presentes = []
    for header, descripcion in headers_fingerprinting.items():
        if request.headers.get(header):
            reduccion = 5
            puntuacion_actual -= reduccion
            headers_presentes.append(f"{header} ({descripcion})")
    
    if headers_presentes:
        detalles_evaluacion.append({
            'factor': f'Headers de fingerprinting detectados',
            'impacto': f'-{len(headers_presentes) * 5} puntos',
            'explicacion': f'Headers presentes: {", ".join(headers_presentes)}',
            'mejora': 'Usar navegadores con resistencia a fingerprinting como Firefox con configuración endurecida'
        })
        recomendaciones_mejora.append('🛡️ Firefox endurecido: Activar "privacy.resistFingerprinting" en about:config')
    else:
        factores_positivos.append({
            'factor': 'Sin headers de fingerprinting detectados',
            'beneficio': '+0 puntos (bueno)',
            'explicacion': 'Tu navegador no está enviando información identificativa extra'
        })
    
    # Evaluar User-Agent
    user_agent = request.headers.get('User-Agent', '')
    if 'Chrome' in user_agent and 'Edg' not in user_agent:
        reduccion = 5
        puntuacion_actual -= reduccion
        detalles_evaluacion.append({
            'factor': 'Navegador Chrome detectado',
            'impacto': f'-{reduccion} puntos',
            'explicacion': 'Chrome tiene menos protecciones de privacidad por defecto',
            'mejora': 'Considera usar Firefox o navegadores orientados a privacidad'
        })
        recomendaciones_mejora.append('🌐 Cambiar navegador: Firefox, Brave, o Tor Browser para mejor privacidad')
    
    puntuacion_final = max(0, min(100, puntuacion_actual))
    
    return {
        'puntuacion': puntuacion_final,
        'puntuacion_inicial': puntuacion_inicial,
        'detalles_evaluacion': detalles_evaluacion,
        'factores_positivos': factores_positivos,
        'recomendaciones_mejora': recomendaciones_mejora,
        'nivel': 'EXCELENTE' if puntuacion_final >= 80 else 'BUENA' if puntuacion_final >= 60 else 'REGULAR' if puntuacion_final >= 40 else 'DEFICIENTE'
    }

def evaluar_riesgo_seguimiento(request):
    """Evaluar el riesgo de seguimiento basado en la solicitud"""
    factores_riesgo = []
    
    if len(request.cookies) > 5:
        factores_riesgo.append("Muchas cookies presentes")
    
    if request.headers.get('Referer'):
        factores_riesgo.append("Header Referer expone historial de navegación")
    
    if not request.headers.get('DNT'):
        factores_riesgo.append("Preferencia No Rastrear no establecida")
    
    if any(request.headers.get(h) for h in ['Sec-Ch-Ua', 'Sec-Ch-Ua-Platform']):
        factores_riesgo.append("Headers de fingerprinting del navegador presentes")
    
    if not request.is_secure:
        factores_riesgo.append("Conexión no segura (HTTP)")
    
    if len(factores_riesgo) >= 4:
        nivel = "MUY ALTO"
    elif len(factores_riesgo) >= 3:
        nivel = "ALTO"
    elif len(factores_riesgo) >= 2:
        nivel = "MODERADO"
    else:
        nivel = "BAJO"
    
    return {
        'nivel': nivel,
        'factores': factores_riesgo
    }

def calcular_resistencia_huella(datos_cliente):
    """Calcular la resistencia a fingerprinting del navegador"""
    puntuacion_resistencia = 100
    factores_vulnerabilidad = []
    recomendaciones = []
    
    # Verificar Canvas fingerprinting
    if datos_cliente.get('huella_canvas') and datos_cliente['huella_canvas'] != 'No disponible':
        puntuacion_resistencia -= 25
        factores_vulnerabilidad.append("Canvas fingerprinting habilitado")
        recomendaciones.append("Usar extensión Canvas Blocker")
    
    # Verificar WebGL fingerprinting
    if datos_cliente.get('huella_webgl') and 'WebGL no disponible' not in str(datos_cliente['huella_webgl']):
        puntuacion_resistencia -= 20
        factores_vulnerabilidad.append("WebGL fingerprinting habilitado")
        recomendaciones.append("Deshabilitar WebGL en sitios no confiables")
    
    # Verificar número de plugins
    plugins = datos_cliente.get('plugins', [])
    if len(plugins) > 5:
        puntuacion_resistencia -= 15
        factores_vulnerabilidad.append("Muchos plugins detectables")
        recomendaciones.append("Reducir número de plugins instalados")
    
    # Verificar información de hardware
    hardware_info = datos_cliente.get('info_navegador', {})
    if hardware_info.get('hardwareConcurrency', 0) > 0:
        puntuacion_resistencia -= 10
        factores_vulnerabilidad.append("Información de hardware expuesta")
        recomendaciones.append("Usar navegador con resistencia a fingerprinting")
    
    # Verificar resolución de pantalla única
    ancho = datos_cliente.get('ancho_pantalla', 0)
    alto = datos_cliente.get('alto_pantalla', 0)
    if ancho and alto:
        # Resoluciones comunes son menos identificables
        resoluciones_comunes = [
            (1920, 1080), (1366, 768), (1280, 720), (1440, 900),
            (1536, 864), (1600, 900), (1024, 768)
        ]
        if (ancho, alto) not in resoluciones_comunes:
            puntuacion_resistencia -= 15
            factores_vulnerabilidad.append("Resolución de pantalla poco común")
            recomendaciones.append("Considerar cambiar resolución a una más común")
    
    # Determinar nivel de resistencia
    if puntuacion_resistencia >= 80:
        nivel = "ALTA"
        explicacion = "Tu navegador tiene buena resistencia al fingerprinting"
    elif puntuacion_resistencia >= 60:
        nivel = "MODERADA"
        explicacion = "Tu navegador tiene resistencia moderada al fingerprinting"
    elif puntuacion_resistencia >= 40:
        nivel = "BAJA"
        explicacion = "Tu navegador es vulnerable al fingerprinting"
    else:
        nivel = "MUY BAJA"
        explicacion = "Tu navegador es muy vulnerable al fingerprinting"
    
    return {
        'nivel': nivel,
        'puntuacion': puntuacion_resistencia,
        'explicacion': explicacion,
        'factores_vulnerabilidad': factores_vulnerabilidad,
        'recomendaciones': recomendaciones
    }

@app.route('/')
def indice():
    """Página principal con la demostración"""
    return render_template_string(PAGINA_DEMO)

@app.route('/analizar', methods=['GET', 'POST'])
def analizar_solicitud():
    """Analizar la solicitud y devolver información completa de exposición de datos con explicaciones en español"""
    # Obtener IP del cliente (manejar proxies/balanceadores de carga)
    ip_cliente = request.headers.get('X-Forwarded-For', 
                request.headers.get('X-Real-IP', 
                request.remote_addr)).split(',')[0].strip()
    
    # Obtener datos de ubicación
    datos_ubicacion = obtener_ubicacion_ip(ip_cliente)
    
    # Analizar user agent
    user_agent = request.headers.get('User-Agent', 'Desconocido')
    so_info, info_navegador = analizar_user_agent(user_agent)
    
    # Obtener datos del lado del cliente
    datos_cliente = request.get_json() or {}
    
    # Calcular resistencia a fingerprinting
    resistencia_huella = calcular_resistencia_huella(datos_cliente)
    
    # Calcular evaluación detallada de privacidad
    evaluacion_privacidad = calcular_puntuacion_privacidad(request)
    
    # Recopilar datos completos con explicaciones en español
    datos_exposicion = {
        # Información de Red
        'direccion_ip': ip_cliente,
        'explicacion_ip': 'Tu dirección única de internet que los sitios web usan para enviarte datos de vuelta. Esto puede revelar tu ubicación aproximada y proveedor de internet.',
        
        'ubicacion': f"{datos_ubicacion['ciudad']}, {datos_ubicacion['region']}, {datos_ubicacion['pais']}",
        'explicacion_ubicacion': 'Tu ubicación física aproximada basada en tu dirección IP. Precisa dentro de un radio de 1-50km.',
        
        'isp': datos_ubicacion['isp'],
        'explicacion_isp': 'Tu Proveedor de Servicios de Internet - la empresa a la que pagas por acceso a internet. Esto puede revelar tu área general y tipo de conexión.',
        
        'tipo_conexion': 'Banda Ancha/Móvil' if not ip_cliente.startswith(('127.', '192.168.')) else 'Local',
        'explicacion_conexion': 'El tipo de conexión a internet que estás usando (WiFi, datos móviles, cable, etc.).',
        
        # Información de Dispositivo y Navegador
        'info_so': so_info,
        'explicacion_so': 'Tu sistema operativo (Windows, Mac, iPhone, etc.). Esto ayuda a los sitios web a optimizar el contenido para tu dispositivo.',
        
        'navegador': info_navegador,
        'explicacion_navegador': 'Tu software de navegador web. Diferentes navegadores tienen diferentes capacidades y características de seguridad.',
        
        'user_agent': user_agent,
        'explicacion_user_agent': 'Una cadena detallada que identifica tu navegador, sistema operativo y dispositivo. Esto es como una huella digital.',
        
        'idioma': request.headers.get('Accept-Language', 'Desconocido').split(',')[0],
        'explicacion_idioma': 'Tu configuración de idioma preferido. Esto puede revelar tu región geográfica y trasfondo cultural.',
        
        'no_rastrear': request.headers.get('DNT', 'No establecido'),
        'explicacion_nrt': 'Una configuración que dice a los sitios web que no quieres ser rastreado. Sin embargo, los sitios web pueden ignorar esta preferencia.',
        
        # Detalles de Pantalla y Dispositivo (del lado del cliente)
        'info_pantalla': f"{datos_cliente.get('ancho_pantalla', 'Desconocido')} x {datos_cliente.get('alto_pantalla', 'Desconocido')} píxeles",
        'explicacion_pantalla': 'Tu resolución de pantalla. Esto ayuda a crear una huella única de tu dispositivo y puede revelar tu tipo de dispositivo.',
        
        'zona_horaria': datos_cliente.get('zona_horaria', 'Desconocido'),
        'explicacion_zona_horaria': 'Tu configuración de zona horaria. Esto puede revelar tu ubicación geográfica y patrones diarios.',
        
        'relacion_pixeles_dispositivo': datos_cliente.get('relacion_pixeles_dispositivo', 'Desconocido'),
        'explicacion_pixel_ratio': 'Cómo tu dispositivo muestra los píxeles. Las pantallas de alta densidad tienen diferentes proporciones, ayudando a identificar tipos de dispositivos.',
        
        # Cookies y Seguimiento
        'cookies': dict(request.cookies) if request.cookies else {},
        'contador_cookies': len(request.cookies) if request.cookies else 0,
        'explicacion_cookies': 'Pequeños archivos almacenados en tu dispositivo que recuerdan información sobre ti. Estos pueden rastrearte a través de sitios web.',
        
        'tiene_cookies_sesion': any('sesion' in k.lower() or 'session' in k.lower() for k in request.cookies.keys()) if request.cookies else False,
        'explicacion_sesion': 'Cookies temporales que te recuerdan durante tu sesión actual de navegación.',
        
        'tiene_cookies_seguimiento': any(rastreador in k.lower() for k in request.cookies.keys() for rastreador in ['ga', 'fb', 'track', 'analytics', '_utm']) if request.cookies else False,
        'explicacion_seguimiento': 'Cookies usadas por empresas publicitarias para seguirte a través de diferentes sitios web y construir perfiles.',
        
        # Huella Digital del Navegador
        'id_sesion': hashlib.md5((ip_cliente + user_agent).encode()).hexdigest()[:12],
        'explicacion_sesion': 'Un identificador único creado para tu visita actual. Esto puede ser usado para rastrear tus acciones en el sitio web.',
        
        'huella_unica': hashlib.sha256((ip_cliente + user_agent + str(request.headers.get('Accept-Language', ''))).encode()).hexdigest()[:16],
        'explicacion_huella': 'Una firma única creada a partir de las características de tu navegador y dispositivo. Esto puede rastrearte incluso sin cookies.',
        
        'huella_canvas': datos_cliente.get('huella_canvas', 'No disponible'),
        'explicacion_canvas': 'Una firma única creada por cómo tu dispositivo dibuja gráficos. Diferentes dispositivos producen diferentes firmas, siendo altamente identificativa.',
        
        'huella_webgl': datos_cliente.get('huella_webgl', 'No disponible'),
        'explicacion_webgl': 'Información sobre tu tarjeta gráfica y controladores. Esto es altamente único y puede identificar tu dispositivo específico.',
        
        # Headers de Seguridad
        'referer': request.headers.get('Referer', 'Visita directa'),
        'explicacion_referer': 'El sitio web del que viniste antes de visitar esta página. Esto revela tu historial de navegación a los sitios web.',
        
        'origen': request.headers.get('Origin', 'No establecido'),
        'explicacion_origen': 'El sitio web que inició esta solicitud. Usado para seguridad pero puede revelar tus patrones de navegación.',
        
        'sec_fetch_site': request.headers.get('Sec-Fetch-Site', 'No establecido'),
        'explicacion_sec_fetch': 'Headers de seguridad que los navegadores envían para proteger contra ataques, pero también proporcionan datos de fingerprinting.',
        
        'riesgo_seguimiento': evaluar_riesgo_seguimiento(request),
        'explicacion_riesgo': 'Evaluación de qué tan fácilmente las empresas pueden rastrearte y perfilarte basado en los datos que estás compartiendo.',
        
        # Evaluación de Privacidad (Detallada)
        'puntuacion_privacidad': evaluacion_privacidad['puntuacion'],
        'evaluacion_detallada': evaluacion_privacidad,
        'explicacion_puntuacion': f'Tu nivel de protección de privacidad es {evaluacion_privacidad["nivel"]} ({evaluacion_privacidad["puntuacion"]}/100). Esta puntuación se calcula evaluando múltiples factores de riesgo.',
        
        # Capacidades de Almacenamiento
        'info_almacenamiento': datos_cliente.get('info_almacenamiento', {}),
        'explicacion_almacenamiento': 'Qué tipos de almacenamiento de datos soporta tu navegador. Los sitios web pueden usar estos para almacenar información de seguimiento.',
        
        # Información de Hardware
        'info_hardware': datos_cliente.get('info_navegador', {}).get('concurrenciaHardware', 'Desconocido'),
        'explicacion_hardware': 'Información sobre el poder de procesamiento de tu dispositivo. Esto ayuda a crear una huella única del dispositivo.',
        
        'plugins': datos_cliente.get('plugins', []),
        'explicacion_plugins': 'Extensiones de software instaladas en tu navegador. La combinación de plugins puede identificarte de manera única.',
        
        # Resistencia a Fingerprinting
        'resistencia_huella': resistencia_huella,
        
        # Timestamp
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        
        # Datos completos para usuarios técnicos
        'datos_tecnicos': {
            'todos_los_headers': dict(request.headers),
            'detalles_solicitud': {
                'metodo': request.method,
                'url': request.url,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
                'es_seguro': request.is_secure,
                'ruta_completa': request.full_path,
                'parametros_query': dict(request.args),
                'datos_formulario': dict(request.form) if request.form else {},
                'datos_json': datos_cliente
            }
        }
    }
    
    return jsonify(datos_exposicion)

@app.route('/establecer-cookies-demo')
def establecer_cookies_demo():
    """Establecer cookies de demostración para mostrar el seguimiento"""
    from flask import make_response
    
    respuesta = make_response(jsonify({
        'mensaje': 'Cookies de demostración establecidas',
        'cookies_creadas': [
            'rastreador_analytics',
            'id_sesion_demo', 
            'preferencias_usuario',
            'ultimo_visitado',
            'cookie_publicitaria'
        ]
    }))
    
    # Establecer varias cookies de demostración
    respuesta.set_cookie('rastreador_analytics', 'GA1.2.123456789.0987654321', max_age=30*24*60*60)
    respuesta.set_cookie('id_sesion_demo', 'ses_' + hashlib.md5(str(datetime.now()).encode()).hexdigest()[:16])
    respuesta.set_cookie('preferencias_usuario', 'idioma=es&tema=oscuro&notificaciones=si')
    respuesta.set_cookie('ultimo_visitado', datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    respuesta.set_cookie('cookie_publicitaria', 'anuncio_' + hashlib.sha1(str(datetime.now()).encode()).hexdigest()[:12])
    
    return respuesta

@app.route('/limpiar-cookies')
def limpiar_cookies():
    """Limpiar todas las cookies para mostrar la diferencia"""
    from flask import make_response
    
    respuesta = make_response(jsonify({
        'mensaje': 'Todas las cookies han sido eliminadas',
        'cookies_eliminadas': list(request.cookies.keys()) if request.cookies else []
    }))
    
    # Eliminar todas las cookies existentes
    if request.cookies:
        for cookie_name in request.cookies.keys():
            respuesta.set_cookie(cookie_name, '', expires=0)
    
    return respuesta

@app.route('/prueba-huella-digital')
def prueba_huella_digital():
    """Endpoint especializado para pruebas de huella digital"""
    user_agent = request.headers.get('User-Agent', '')
    accept_headers = request.headers.get('Accept', '')
    accept_language = request.headers.get('Accept-Language', '')
    accept_encoding = request.headers.get('Accept-Encoding', '')
    
    # Crear una huella digital más detallada
    huella_completa = f"{user_agent}{accept_headers}{accept_language}{accept_encoding}"
    huella_hash = hashlib.sha256(huella_completa.encode()).hexdigest()
    
    return jsonify({
        'huella_digital': {
            'hash_completo': huella_hash,
            'componentes': {
                'user_agent': user_agent,
                'accept_headers': accept_headers,
                'accept_language': accept_language,
                'accept_encoding': accept_encoding
            },
            'unicidad_estimada': len(set(huella_completa)) / len(huella_completa) if huella_completa else 0,
            'explicacion': 'Esta huella digital combina múltiples características de tu navegador para crear un identificador único'
        }
    })

@app.route('/consejos-privacidad')
def consejos_privacidad():
    """Página con consejos completos de privacidad"""
    consejos = {
        'navegadores_seguros': [
            {
                'nombre': 'Firefox con configuración endurecida',
                'descripcion': 'Mozilla Firefox con about:config modificado para máxima privacidad',
                'nivel': 'Intermedio',
                'pasos': [
                    'Descargar Firefox desde mozilla.org',
                    'Ir a about:config',
                    'Establecer privacy.resistFingerprinting = true',
                    'Establecer privacy.trackingprotection.enabled = true',
                    'Deshabilitar WebRTC y geolocalización'
                ]
            },
            {
                'nombre': 'Tor Browser',
                'descripcion': 'El navegador más privado disponible, enruta tráfico a través de la red Tor',
                'nivel': 'Avanzado',
                'pasos': [
                    'Descargar desde torproject.org',
                    'Verificar firmas criptográficas',
                    'Usar siempre en pantalla completa',
                    'No instalar extensiones adicionales',
                    'No iniciar sesión en cuentas personales'
                ]
            }
        ],
        'extensiones_privacidad': [
            {
                'nombre': 'uBlock Origin',
                'proposito': 'Bloquea anuncios, rastreadores y malware',
                'instalacion': 'Disponible en tiendas oficiales de extensiones'
            },
            {
                'nombre': 'Privacy Badger',
                'proposito': 'Bloquea rastreadores automáticamente',
                'instalacion': 'Desarrollado por Electronic Frontier Foundation'
            },
            {
                'nombre': 'ClearURLs',
                'proposito': 'Elimina parámetros de seguimiento de URLs',
                'instalacion': 'Limpia automáticamente enlaces maliciosos'
            },
            {
                'nombre': 'Canvas Blocker',
                'proposito': 'Previene fingerprinting por canvas HTML5',
                'instalacion': 'Falsifica o bloquea lecturas de canvas'
            }
        ],
        'vpn_recomendadas': [
            {
                'categoria': 'Máxima Privacidad',
                'opciones': ['Mullvad VPN', 'IVPN', 'ProtonVPN'],
                'caracteristicas': ['Sin logs', 'Pagos anónimos', 'Jurisdicciones favorables']
            },
            {
                'categoria': 'Equilibrio Precio/Privacidad',
                'opciones': ['Surfshark', 'NordVPN', 'ExpressVPN'],
                'caracteristicas': ['Buena velocidad', 'Muchos servidores', 'Aplicaciones fáciles']
            }
        ],
        'configuraciones_dispositivo': {
            'telefono': [
                'Deshabilitar ubicación en aplicaciones innecesarias',
                'Usar DNS privados (1.1.1.1 o 9.9.9.9)',
                'Revisar permisos de aplicaciones regularmente',
                'Usar tiendas de aplicaciones alternativas (F-Droid para Android)'
            ],
            'computadora': [
                'Usar sistema operativo enfocado en privacidad (Linux)',
                'Cifrar disco duro completo',
                'Usar firewall local',
                'Revisar aplicaciones que se inician automáticamente'
            ]
        },
        'habitos_seguros': [
            'Usar diferentes contraseñas para cada servicio',
            'Habilitar autenticación de dos factores',
            'Revisar configuraciones de privacidad regularmente',
            'Leer políticas de privacidad antes de usar servicios',
            'Usar motores de búsqueda privados (DuckDuckGo, Startpage)',
            'Evitar redes WiFi públicas para actividades sensibles'
        ]
    }
    
    return jsonify({
        'titulo': 'Guía Completa de Privacidad Digital',
        'consejos': consejos,
        'mensaje': 'La privacidad es un derecho fundamental. Estos consejos te ayudarán a protegerla.',
        'actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    })

@app.route('/salud')
def verificar_salud():
    """Endpoint de verificación de salud"""
    return jsonify({
        'estado': 'activo',
        'servicio': 'Servidor de Análisis de Exposición de Datos - Edición Revelada (Español)',
        'version': '2.0',
        'endpoints_disponibles': [
            '/ - Página principal de demostración',
            '/analizar - Análisis completo de exposición de datos',
            '/establecer-cookies-demo - Establecer cookies de demostración',
            '/limpiar-cookies - Eliminar todas las cookies',
            '/prueba-huella-digital - Prueba especializada de fingerprinting',
            '/consejos-privacidad - Guía completa de privacidad',
            '/reporte-privacidad - Reporte detallado personalizado',
            '/comparar-navegadores - Comparación de navegadores por privacidad',
            '/prueba-configuracion - Probar configuración de privacidad actual',
            '/salud - Este endpoint de estado'
        ],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    })

@app.route('/reporte-privacidad')
def generar_reporte_privacidad():
    """Generar un reporte detallado de privacidad para el usuario"""
    ip_cliente = request.headers.get('X-Forwarded-For', 
                request.headers.get('X-Real-IP', 
                request.remote_addr)).split(',')[0].strip()
    
    datos_ubicacion = obtener_ubicacion_ip(ip_cliente)
    user_agent = request.headers.get('User-Agent', 'Desconocido')
    so_info, info_navegador = analizar_user_agent(user_agent)
    
    reporte = {
        'fecha_reporte': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'resumen_ejecutivo': {
            'puntuacion_privacidad': calcular_puntuacion_privacidad(request),
            'nivel_riesgo': evaluar_riesgo_seguimiento(request)['nivel'],
            'recomendacion_principal': 'Usar VPN y bloquear rastreadores'
        },
        'analisis_detallado': {
            'exposicion_red': {
                'ip_visible': ip_cliente,
                'ubicacion_aproximada': f"{datos_ubicacion['ciudad']}, {datos_ubicacion['pais']}",
                'proveedor_internet': datos_ubicacion['isp'],
                'riesgo': 'ALTO' if not ip_cliente.startswith(('127.', '192.168.')) else 'BAJO'
            },
            'huella_navegador': {
                'sistema_operativo': so_info,
                'navegador': info_navegador,
                'idioma': request.headers.get('Accept-Language', 'Desconocido').split(',')[0],
                'cookies_presentes': len(request.cookies) if request.cookies else 0
            }
        },
        'recomendaciones_personalizadas': [],
        'pasos_inmediatos': [
            'Instalar uBlock Origin en tu navegador',
            'Considerar usar una VPN confiable',
            'Revisar y limpiar cookies regularmente',
            'Configurar Do Not Track en tu navegador'
        ],
        'recursos_adicionales': [
            'https://privacyguides.org - Guías de privacidad actualizadas',
            'https://www.eff.org - Electronic Frontier Foundation',
            'https://duckduckgo.com - Motor de búsqueda privado',
            'https://www.torproject.org - Navegador Tor para máxima privacidad'
        ]
    }
    
    # Generar recomendaciones personalizadas basadas en el análisis
    if len(request.cookies) > 10:
        reporte['recomendaciones_personalizadas'].append(
            'Tienes muchas cookies. Considera limpiarlas regularmente o usar modo incógnito.'
        )
    
    if not request.headers.get('DNT'):
        reporte['recomendaciones_personalizadas'].append(
            'Activa la configuración "Do Not Track" en tu navegador.'
        )
    
    if 'Windows' in so_info:
        reporte['recomendaciones_personalizadas'].append(
            'Como usuario de Windows, considera usar Firefox con configuración endurecida.'
        )
    
    if not request.is_secure:
        reporte['recomendaciones_personalizadas'].append(
            'CRÍTICO: Estás usando una conexión no segura (HTTP). Siempre usa HTTPS.'
        )
    
    return jsonify(reporte)

@app.route('/comparar-navegadores')
def comparar_navegadores():
    """Comparar diferentes navegadores desde una perspectiva de privacidad"""
    comparacion = {
        'metodologia': 'Comparación basada en características de privacidad por defecto',
        'ultima_actualizacion': datetime.now().strftime('%Y-%m-%d'),
        'navegadores': {
            'Tor Browser': {
                'puntuacion_privacidad': 95,
                'ventajas': [
                    'Máxima privacidad y anonimato',
                    'Bloquea fingerprinting por defecto',
                    'Enruta tráfico a través de la red Tor',
                    'No guarda historial por defecto'
                ],
                'desventajas': [
                    'Más lento que otros navegadores',
                    'Algunos sitios pueden bloquearlo',
                    'Curva de aprendizaje para nuevos usuarios'
                ],
                'recomendado_para': 'Usuarios que necesitan máxima privacidad'
            },
            'Firefox (configurado)': {
                'puntuacion_privacidad': 85,
                'ventajas': [
                    'Altamente configurable para privacidad',
                    'Extensiones de privacidad excelentes',
                    'Desarrollado por organización sin fines de lucro',
                    'Resistencia a fingerprinting disponible'
                ],
                'desventajas': [
                    'Requiere configuración manual',
                    'Puede romper algunos sitios web',
                    'Menos soporte para sitios empresariales'
                ],
                'recomendado_para': 'Usuarios técnicos que valoran privacidad'
            },
            'Safari': {
                'puntuacion_privacidad': 70,
                'ventajas': [
                    'Buen bloqueo de rastreadores por defecto',
                    'Integrado con el ecosistema Apple',
                    'Prevención inteligente de seguimiento',
                    'Protección de correo privado'
                ],
                'desventajas': [
                    'Solo disponible en dispositivos Apple',
                    'Menos extensiones de privacidad',
                    'Control limitado sobre configuraciones'
                ],
                'recomendado_para': 'Usuarios del ecosistema Apple'
            },
            'Google Chrome': {
                'puntuacion_privacidad': 40,
                'ventajas': [
                    'Rápido y compatible con la mayoría de sitios',
                    'Sincronización entre dispositivos',
                    'Actualizaciones de seguridad regulares',
                    'Gran ecosistema de extensiones'
                ],
                'desventajas': [
                    'Desarrollado por empresa de publicidad',
                    'Recopila muchos datos por defecto',
                    'Historial de preocupaciones de privacidad',
                    'Fingerprinting habilitado por defecto'
                ],
                'recomendado_para': 'Usuarios que priorizan conveniencia sobre privacidad'
            },
            'Microsoft Edge': {
                'puntuacion_privacidad': 50,
                'ventajas': [
                    'Mejores características de privacidad que Chrome',
                    'Integrado con Windows',
                    'Prevención de seguimiento configurable',
                    'Microsoft Defender integrado'
                ],
                'desventajas': [
                    'Desarrollado por Microsoft (preocupaciones de datos)',
                    'Menos maduro en características de privacidad',
                    'Telemetría habilitada por defecto'
                ],
                'recomendado_para': 'Usuarios de Windows que quieren mejor privacidad que Chrome'
            }
        },
        'recomendaciones_generales': [
            'Para máxima privacidad: Tor Browser',
            'Para uso diario con buena privacidad: Firefox configurado',
            'Para usuarios de Apple: Safari con configuraciones endurecidas',
            'Evitar: Chrome sin extensiones de privacidad'
        ]
    }
    
    return jsonify(comparacion)

@app.route('/prueba-configuracion')
def probar_configuracion_privacidad():
    """Probar qué tan bien está configurado el navegador para privacidad"""
    resultados_prueba = {
        'fecha_prueba': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'puntuacion_total': 0,
        'pruebas': {}
    }
    
    # Prueba 1: Do Not Track
    dnt = request.headers.get('DNT')
    if dnt == '1':
        resultados_prueba['pruebas']['do_not_track'] = {
            'estado': 'APROBADO',
            'puntos': 10,
            'descripcion': 'Do Not Track está habilitado'
        }
        resultados_prueba['puntuacion_total'] += 10
    else:
        resultados_prueba['pruebas']['do_not_track'] = {
            'estado': 'FALLO',
            'puntos': 0,
            'descripcion': 'Do Not Track no está habilitado',
            'solucion': 'Activa DNT en configuración del navegador'
        }
    
    # Prueba 2: Cantidad de cookies
    num_cookies = len(request.cookies) if request.cookies else 0
    if num_cookies == 0:
        resultados_prueba['pruebas']['cookies'] = {
            'estado': 'EXCELENTE',
            'puntos': 20,
            'descripcion': 'Sin cookies detectadas'
        }
        resultados_prueba['puntuacion_total'] += 20
    elif num_cookies <= 5:
        resultados_prueba['pruebas']['cookies'] = {
            'estado': 'BUENO',
            'puntos': 15,
            'descripcion': f'Pocas cookies detectadas ({num_cookies})'
        }
        resultados_prueba['puntuacion_total'] += 15
    elif num_cookies <= 10:
        resultados_prueba['pruebas']['cookies'] = {
            'estado': 'ADVERTENCIA',
            'puntos': 10,
            'descripcion': f'Cantidad moderada de cookies ({num_cookies})'
        }
        resultados_prueba['puntuacion_total'] += 10
    else:
        resultados_prueba['pruebas']['cookies'] = {
            'estado': 'FALLO',
            'puntos': 0,
            'descripcion': f'Demasiadas cookies ({num_cookies})',
            'solucion': 'Limpia cookies regularmente o usa modo incógnito'
        }
    
    # Prueba 3: Conexión segura
    if request.is_secure:
        resultados_prueba['pruebas']['conexion_segura'] = {
            'estado': 'APROBADO',
            'puntos': 15,
            'descripcion': 'Usando conexión HTTPS segura'
        }
        resultados_prueba['puntuacion_total'] += 15
    else:
        resultados_prueba['pruebas']['conexion_segura'] = {
            'estado': 'CRÍTICO',
            'puntos': 0,
            'descripcion': 'Usando conexión HTTP insegura',
            'solucion': 'Siempre usa HTTPS. Instala extensión HTTPS Everywhere'
        }
    
    # Prueba 4: Headers de fingerprinting
    headers_fp = ['Sec-Ch-Ua', 'Sec-Ch-Ua-Platform', 'Sec-Ch-Ua-Mobile']
    headers_detectados = [h for h in headers_fp if request.headers.get(h)]
    
    if len(headers_detectados) == 0:
        resultados_prueba['pruebas']['fingerprinting_headers'] = {
            'estado': 'EXCELENTE',
            'puntos': 15,
            'descripcion': 'Sin headers de fingerprinting detectados'
        }
        resultados_prueba['puntuacion_total'] += 15
    elif len(headers_detectados) <= 2:
        resultados_prueba['pruebas']['fingerprinting_headers'] = {
            'estado': 'ADVERTENCIA',
            'puntos': 5,
            'descripcion': f'Algunos headers de fingerprinting presentes ({len(headers_detectados)})'
        }
        resultados_prueba['puntuacion_total'] += 5
    else:
        resultados_prueba['pruebas']['fingerprinting_headers'] = {
            'estado': 'FALLO',
            'puntos': 0,
            'descripcion': 'Muchos headers de fingerprinting detectados',
            'solucion': 'Usa Firefox con privacy.resistFingerprinting=true'
        }
    
    # Prueba 5: Referer header
    referer = request.headers.get('Referer')
    if not referer:
        resultados_prueba['pruebas']['referer_header'] = {
            'estado': 'APROBADO',
            'puntos': 10,
            'descripcion': 'Sin header Referer que exponga historial'
        }
        resultados_prueba['puntuacion_total'] += 10
    else:
        resultados_prueba['pruebas']['referer_header'] = {
            'estado': 'FALLO',
            'puntos': 0,
            'descripcion': 'Header Referer presente, expone historial de navegación',
            'solucion': 'Configura navegador para no enviar referer o usar extensión'
        }
    
    # Determinar nivel general
    if resultados_prueba['puntuacion_total'] >= 60:
        nivel = 'EXCELENTE'
        mensaje = 'Tu configuración de privacidad es muy buena'
    elif resultados_prueba['puntuacion_total'] >= 40:
        nivel = 'BUENO'
        mensaje = 'Tu configuración de privacidad es decente pero mejorable'
    elif resultados_prueba['puntuacion_total'] >= 20:
        nivel = 'REGULAR'
        mensaje = 'Tu configuración de privacidad necesita mejoras'
    else:
        nivel = 'CRÍTICO'
        mensaje = 'Tu configuración de privacidad está muy expuesta'
    
    resultados_prueba['nivel_general'] = nivel
    resultados_prueba['mensaje'] = mensaje
    resultados_prueba['puntuacion_maxima'] = 70
    
    return jsonify(resultados_prueba)

if __name__ == '__main__':
    print("🕵️ SERVIDOR DE ANÁLISIS DE EXPOSICIÓN DE DATOS - EDICIÓN REVELADA (ESPAÑOL)")
    print("=" * 80)
    print("🚨 ADVERTENCIA: Esta es una herramienta educativa de ciberseguridad")
    print("📚 Propósito: Demostrar qué datos pueden recopilar los sitios web")
    print("🛡️ Usar para: Educación en privacidad y concienciación en seguridad")
    print()
    print("🌐 Servidor iniciándose en: http://localhost:5000")
    print("📖 Documentación de API: http://localhost:5000/salud")
    print()
    print("⚠️  RECUERDA: Los sitios web reales pueden recopilar TODA esta información")
    print("🔒 PROTÉGETE: Usa VPN, bloqueadores de anuncios y navegadores seguros")
    print("=" * 80)
    
    # Ejecutar servidor Flask
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
