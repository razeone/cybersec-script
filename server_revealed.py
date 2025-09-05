#!/usr/bin/env python3
"""
🔍 HTTP REQUEST DATA EXPOSURE DEMONSTRATION (REVEALED Edition)
Shows participants exactly what data they reveal with every web request
Perfect for cybersecurity awareness training!
Enhanced with detailed explanations and privacy education
"""

from flask import Flask, request, jsonify, render_template_string, make_response
import socket
import json
from datetime import datetime
import os
import requests
import hashlib

app = Flask(__name__)

# HTML template for the demo page with enhanced explanations
DEMO_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>🔍 Data Exposure REVEALED - What Websites Really Know About You!</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 1200px; 
            margin: 30px auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            line-height: 1.6;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 { text-align: center; font-size: 2.5em; margin-bottom: 30px; }
        h2 { color: #4ecdc4; margin-top: 25px; }
        h3 { color: #4ecdc4; margin-top: 20px; }
        .warning { 
            background: #ff6b6b; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
        }
        .reveal-btn {
            background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
            color: white;
            padding: 20px 40px;
            font-size: 1.5em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            display: block;
            margin: 30px auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        .reveal-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        }
        .demo-controls {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .demo-btn {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .demo-btn:hover { background: #45a049; }
        .demo-btn.danger { background: #f44336; }
        .demo-btn.danger:hover { background: #da190b; }
        #results {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            max-height: 600px;
            overflow-y: auto;
            display: none;
        }
        .privacy-score {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-weight: bold;
            text-align: center;
            font-size: 1.2em;
        }
        .score-high { background: #4CAF50; }
        .score-medium { background: #FF9800; }
        .score-low { background: #f44336; }
        .data-section {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .data-item {
            margin: 10px 0;
            padding: 8px;
            background: rgba(255,255,255,0.05);
            border-radius: 5px;
        }
        .data-label {
            font-weight: bold;
            color: #4ecdc4;
            margin-bottom: 5px;
        }
        .data-value {
            color: #ff6b6b;
            font-family: monospace;
            margin-bottom: 5px;
        }
        .data-explanation {
            font-style: italic;
            color: #ffffff;
            opacity: 0.9;
            font-size: 0.9em;
        }
        .risk-section {
            background: rgba(255,107,107,0.2);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #ff6b6b;
        }
        .protection-section {
            background: rgba(76,175,80,0.2);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #4CAF50;
        }
        .protection-tip {
            margin: 8px 0;
            padding: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
        }
        .tip-title {
            font-weight: bold;
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Data Exposure REVEALED</h1>
        
        <div class="warning">
            ⚠️ WARNING: This demonstration will reveal EXTENSIVE information about your device and browsing habits!
            You'll see exactly what companies collect about you every time you visit a website.
        </div>
        
        <div class="demo-controls">
            <h3>Demo Controls:</h3>
            <button class="demo-btn" onclick="setCookies()">🍪 Set Demo Cookies</button>
            <button class="demo-btn danger" onclick="clearCookies()">🗑️ Clear Cookies</button>
            <button class="demo-btn" onclick="showFingerprint()">👆 Browser Fingerprint</button>
        </div>
        
        <p style="text-align: center; font-size: 1.2em;">
            Click the button below to see exactly what information websites can collect about you,
            with detailed explanations of what each piece of data means and why it matters:
        </p>
        
        <button class="reveal-btn" onclick="revealDataExposure()">
            🕵️ REVEAL WHAT WEBSITES KNOW ABOUT ME 🕵️
        </button>
        
        <div id="results"></div>
        
        <div style="margin-top: 30px; text-align: center; font-size: 0.9em; opacity: 0.8;">
            <p>🎯 Educational Purpose: Understanding Digital Privacy & Data Collection</p>
            <p>Visit <a href="/privacy-tips" style="color: #FFD700;">Privacy Tips</a> for comprehensive protection strategies</p>
        </div>
    </div>

    <script>
        // Set demo cookies
        function setCookies() {
            fetch('/set-demo-cookies')
                .then(response => response.json())
                .then(data => {
                    alert('Demo cookies set! Refresh the page and run the analysis again to see the difference.');
                });
        }
        
        // Clear demo cookies
        function clearCookies() {
            fetch('/clear-cookies')
                .then(response => response.json())
                .then(data => {
                    alert('Demo cookies cleared! Refresh the page and run the analysis again.');
                });
        }
        
        // Show fingerprint data
        function showFingerprint() {
            fetch('/fingerprint-test')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('results').style.display = 'block';
                    document.getElementById('results').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                });
        }
        
        // Main data exposure function with enhanced explanations
        function revealDataExposure() {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = '<div style="text-align: center; font-size: 1.2em;">🔍 Analyzing your digital footprint... Please wait...</div>';
            
            // Include comprehensive client-side data
            const clientData = JSON.stringify(window.clientInfo || {});
            
            fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: clientData
            })
            .then(response => response.json())
            .then(data => {
                displayExplainedResults(data);
            })
            .catch(error => {
                resultsDiv.innerHTML = '<div style="color: #ff6b6b;">Error collecting data: ' + error + '</div>';
            });
        }
        
        function displayExplainedResults(data) {
            const resultsDiv = document.getElementById('results');
            
            let html = '<div style="color: #ff6b6b; text-align: center; margin-bottom: 20px; font-size: 1.3em;">' +
                      '🚨 HERE\\'S WHAT WEBSITES CAN SEE ABOUT YOU 🚨' +
                      '</div>';
            
            // Privacy Score with explanation
            const score = data.privacy_score || 50;
            const scoreClass = score > 70 ? 'score-high' : score > 40 ? 'score-medium' : 'score-low';
            const scoreText = score > 70 ? 'GOOD PRIVACY' : score > 40 ? 'MODERATE PRIVACY' : 'POOR PRIVACY';
            
            html += '<div class="privacy-score ' + scoreClass + '">' +
                   '🛡️ Your Privacy Score: ' + score + '/100 (' + scoreText + ')' +
                   '</div>';
            html += '<div style="font-style: italic; margin-bottom: 20px; text-align: center;">' + 
                   (data.score_explanation || 'Your privacy protection level. Lower scores mean you\\'re easier to track and profile.') + 
                   '</div>';
            
            // Location & Network Section
            html += createExplainedSection('📍 Your Location & Internet Connection', [
                {
                    label: 'Your Internet Address (IP)',
                    value: data.ip_address,
                    explanation: data.ip_explanation || 'Your unique internet address that websites use to send data back to you. This can reveal your approximate location and internet provider.'
                },
                {
                    label: 'Your Approximate Location',
                    value: data.location,
                    explanation: data.location_explanation || 'Your approximate physical location based on your IP address. Accurate within 1-50km radius.'
                },
                {
                    label: 'Your Internet Provider (ISP)',
                    value: data.isp,
                    explanation: data.isp_explanation || 'Your Internet Service Provider - the company you pay for internet access. This can reveal your general area and connection type.'
                },
                {
                    label: 'Connection Type',
                    value: data.connection_type,
                    explanation: data.connection_explanation || 'The type of internet connection you\\'re using (WiFi, mobile data, wired, etc.).'
                }
            ]);
            
            // Device & Browser Section
            html += createExplainedSection('💻 Your Device & Browser Information', [
                {
                    label: 'Operating System',
                    value: data.os_info,
                    explanation: data.os_explanation || 'Your operating system (Windows, Mac, iPhone, etc.). This helps websites optimize content for your device.'
                },
                {
                    label: 'Web Browser',
                    value: data.browser,
                    explanation: data.browser_explanation || 'Your web browser software. Different browsers have different capabilities and security features.'
                },
                {
                    label: 'Screen Resolution',
                    value: (window.clientInfo ? window.clientInfo.screen_width + 'x' + window.clientInfo.screen_height : 'Unknown') + ' pixels',
                    explanation: data.screen_explanation || 'Your screen resolution. This helps create a unique fingerprint of your device and can reveal your device type.'
                },
                {
                    label: 'Time Zone',
                    value: window.clientInfo ? window.clientInfo.timezone : 'Unknown',
                    explanation: data.timezone_explanation || 'Your time zone setting. This can reveal your geographic location and daily patterns.'
                },
                {
                    label: 'Language Preference',
                    value: data.language,
                    explanation: data.language_explanation || 'Your preferred language settings. This can reveal your geographic region and cultural background.'
                },
                {
                    label: 'Device Pixel Ratio',
                    value: window.clientInfo ? window.clientInfo.device_pixel_ratio : 'Unknown',
                    explanation: data.pixel_ratio_explanation || 'How your device displays pixels. High-DPI displays have different ratios, helping identify device types.'
                }
            ]);
            
            // Tracking & Privacy Section
            html += createExplainedSection('🕵️ Tracking & Privacy Information', [
                {
                    label: 'Cookies on Your Device',
                    value: data.cookie_count + ' cookies found',
                    explanation: data.cookie_explanation || 'Small files stored on your device that remember information about you. These can track your visits across websites.'
                },
                {
                    label: 'Session Cookies',
                    value: data.has_session_cookies ? 'YES - Active session tracking' : 'None detected',
                    explanation: data.session_explanation || 'Temporary cookies that remember you during your current browsing session.'
                },
                {
                    label: 'Tracking Cookies',
                    value: data.has_tracking_cookies ? 'YES - You are being tracked!' : 'None detected',
                    explanation: data.tracking_explanation || 'Cookies used by advertising companies to follow you across different websites and build profiles.'
                },
                {
                    label: 'Do Not Track Setting',
                    value: data.do_not_track,
                    explanation: data.dnt_explanation || 'A setting that tells websites you don\\'t want to be tracked. However, websites can ignore this preference.'
                },
                {
                    label: 'Unique Browser Fingerprint',
                    value: data.unique_fingerprint,
                    explanation: data.fingerprint_explanation || 'A unique signature created from your browser and device characteristics. This can track you even without cookies.'
                }
            ]);
            
            // Advanced Fingerprinting Section
            if (window.clientInfo) {
                html += createExplainedSection('👆 Advanced Browser Fingerprinting', [
                    {
                        label: 'Canvas Fingerprint',
                        value: window.clientInfo.canvas_fingerprint || 'Not available',
                        explanation: data.canvas_explanation || 'Your graphics card and drivers render text/images slightly differently than others. This creates a unique "canvas fingerprint" that\\'s highly stable.'
                    },
                    {
                        label: 'WebGL Fingerprint',
                        value: window.clientInfo.webgl_fingerprint || 'Not available',
                        explanation: data.webgl_explanation || 'Information about your graphics processing unit (GPU). Different graphics cards render 3D graphics differently.'
                    },
                    {
                        label: 'Screen Fingerprint',
                        value: data.screen_fingerprint || 'Unknown',
                        explanation: data.screen_explanation || 'Your exact screen resolution and color depth combined with other factors makes you identifiable.'
                    },
                    {
                        label: 'Language Fingerprint',
                        value: data.language_fingerprint || 'Unknown',
                        explanation: data.language_explanation || 'Your language preferences create a fingerprint. The specific order of languages is often unique.'
                    },
                    {
                        label: 'Timezone Fingerprint',
                        value: data.timezone_fingerprint || 'Unknown',
                        explanation: data.timezone_explanation || 'Your timezone setting reveals geographic location and combines with other data.'
                    },
                    {
                        label: 'Hardware Detection',
                        value: window.clientInfo.navigator_info ? window.clientInfo.navigator_info.hardwareConcurrency + ' CPU cores' : 'Unknown',
                        explanation: data.hardware_explanation || 'Information about your device\\'s processing power helps distinguish device types.'
                    },
                    {
                        label: 'Plugin Count',
                        value: data.plugin_fingerprint ? data.plugin_fingerprint + ' plugins' : 'Unknown',
                        explanation: data.plugin_explanation || 'Each person has a unique combination of browser plugins that can identify them.'
                    },
                    {
                        label: 'Font Detection',
                        value: data.font_detection || 'Available',
                        explanation: data.font_explanation || 'Websites can detect installed fonts. Your unique font collection creates another tracking dimension.'
                    },
                    {
                        label: 'Audio Fingerprinting',
                        value: data.audio_fingerprint || 'Possible',
                        explanation: data.audio_explanation || 'Your audio hardware processes sounds differently, creating a unique audio fingerprint.'
                    }
                ]);
                
                // Fingerprint Resistance Assessment
                if (data.fingerprint_resistance) {
                    const resistance = data.fingerprint_resistance;
                    const resistanceClass = resistance.level === 'HIGH' ? 'score-high' : 
                                          resistance.level === 'MEDIUM' ? 'score-medium' : 'score-low';
                    
                    html += '<div style="background: rgba(255,193,7,0.2); padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #ffc107;">';
                    html += '<h3>🛡️ Your Fingerprint Resistance</h3>';
                    html += '<div class="' + resistanceClass + '" style="font-size: 1.1em; margin: 10px 0;">Score: ' + resistance.score + '/100 (' + resistance.level + ')</div>';
                    html += '<div style="font-style: italic; margin-bottom: 10px;">' + data.resistance_explanation + '</div>';
                    
                    if (resistance.factors && resistance.factors.length > 0) {
                        html += '<div><strong>Resistance Factors:</strong></div><ul>';
                        resistance.factors.forEach(factor => {
                            html += '<li>' + factor + '</li>';
                        });
                        html += '</ul>';
                    }
                    html += '</div>';
                }
            }
            
            // Security Headers Section
            html += createExplainedSection('🔒 Security & Navigation Headers', [
                {
                    label: 'Referer Header',
                    value: data.referer,
                    explanation: data.referer_explanation || 'The website you came from before visiting this page. This reveals your browsing history to websites.'
                },
                {
                    label: 'Origin Header',
                    value: data.origin,
                    explanation: data.origin_explanation || 'The website that initiated this request. Used for security but can reveal your browsing patterns.'
                },
                {
                    label: 'Sec-Fetch Headers',
                    value: data.sec_fetch_site + ', ' + data.sec_fetch_mode,
                    explanation: data.sec_fetch_explanation || 'Security headers that browsers send to protect against attacks, but also provide fingerprinting data.'
                }
            ]);
            
            // Storage Capabilities Section
            if (window.clientInfo && window.clientInfo.storage_info) {
                html += createExplainedSection('💾 Data Storage Capabilities', [
                    {
                        label: 'Local Storage',
                        value: window.clientInfo.storage_info.localStorage ? 'Available' : 'Not available',
                        explanation: data.storage_explanation || 'What types of data storage your browser supports. Websites can use these to store tracking information.'
                    },
                    {
                        label: 'Session Storage',
                        value: window.clientInfo.storage_info.sessionStorage ? 'Available' : 'Not available',
                        explanation: 'Temporary storage that persists only for your current browser session.'
                    }
                ]);
            }
            
            // Privacy Risks Section
            if (data.tracking_risk && data.tracking_risk.factors) {
                html += '<div class="risk-section">';
                html += '<h3>⚠️ Privacy Risks Detected</h3>';
                html += '<div style="font-style: italic; margin-bottom: 10px;">' + 
                       (data.risk_explanation || 'Assessment of how easily companies can track and profile you based on the data you\\'re sharing.') + 
                       '</div>';
                html += '<div><strong>Risk Level:</strong> ' + data.tracking_risk.level + '</div>';
                html += '<div><strong>Specific Risks:</strong></div><ul>';
                data.tracking_risk.factors.forEach(factor => {
                    html += '<li>' + factor + '</li>';
                });
                html += '</ul></div>';
            }
            
            // Active Cookies Details
            if (data.cookies && Object.keys(data.cookies).length > 0) {
                html += '<div class="data-section">';
                html += '<h3>🍪 Active Cookies on Your Device</h3>';
                html += '<div style="font-style: italic; margin-bottom: 10px;">These are the actual cookies stored on your device right now:</div>';
                Object.keys(data.cookies).forEach(cookie => {
                    html += '<div class="data-item">';
                    html += '<div class="data-label">' + cookie + ':</div>';
                    html += '<div class="data-value">' + (data.cookies[cookie].length > 100 ? data.cookies[cookie].substring(0, 100) + '...' : data.cookies[cookie]) + '</div>';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            // Protection Tips Section
            html += '<div class="protection-section">';
            html += '<h3>🛡️ How to Protect Your Privacy</h3>';
            html += '<div style="font-style: italic; margin-bottom: 15px;">Here are actionable steps you can take right now to protect your privacy:</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🔒 Use a VPN:</span> Hide your real IP address and location from websites';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🕵️ Private Browsing:</span> Use incognito/private mode to reduce cookie tracking';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🚫 Ad Blockers:</span> Install uBlock Origin to block trackers and ads';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🧹 Clear Data:</span> Regularly delete cookies, browsing history, and cached data';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🔧 Browser Settings:</span> Enable "Do Not Track" and disable third-party cookies';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🦊 Privacy Browser:</span> Consider Firefox with strict privacy settings or Tor Browser';
            html += '</div>';
            
            html += '</div>';
            
            // Specific Fingerprinting Protection Section
            html += '<div style="background: rgba(255,87,34,0.2); padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #FF5722;">';
            html += '<h3>🔍 How to Reduce Browser Fingerprinting</h3>';
            html += '<div style="margin-bottom: 15px; font-style: italic;">Browser fingerprinting is harder to block than cookies, but these steps help:</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🌐 Use Tor Browser:</span> Best fingerprint protection - makes you look like other Tor users';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🦊 Firefox with Privacy Settings:</span> Enable "Resist Fingerprinting" in about:config';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🚫 Disable WebGL:</span> Type "webgl.disabled" = true in Firefox about:config';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🎨 Block Canvas Access:</span> Use extensions like Canvas Blocker or uBlock Origin';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🔌 Minimize Plugins:</span> Disable or remove unnecessary browser plugins and extensions';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">📱 Use Common Settings:</span> Common screen resolution, timezone, and language reduce uniqueness';
            html += '</div>';
            
            html += '<div class="protection-tip">';
            html += '<span class="tip-title">🔄 Browser Rotation:</span> Regularly switch between different browsers and profiles';
            html += '</div>';
            
            html += '<div style="margin-top: 15px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px;">';
            html += '<strong>⚠️ Important:</strong> Even with these protections, determined trackers may still identify you. ';
            html += 'For maximum privacy, use Tor Browser for sensitive activities.';
            html += '</div>';
            
            html += '</div>';
            
            // Technical Details for Advanced Users
            html += '<div class="data-section" style="margin-top: 30px;">';
            html += '<h3>🔧 Complete Technical Data (For Advanced Users)</h3>';
            html += '<div style="font-style: italic; margin-bottom: 10px;">Raw data that websites collect - click to expand:</div>';
            html += '<details style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px;">';
            html += '<summary style="cursor: pointer; font-weight: bold; color: #4ecdc4;">Click to view raw technical data</summary>';
            html += '<pre style="white-space: pre-wrap; font-size: 0.8em; margin-top: 10px;">' + JSON.stringify(data, null, 2) + '</pre>';
            html += '</details>';
            html += '</div>';
            
            resultsDiv.innerHTML = html;
        }
        
        function createExplainedSection(title, items) {
            let html = '<div class="data-section">';
            html += '<h3>' + title + '</h3>';
            
            items.forEach(item => {
                html += '<div class="data-item">';
                html += '<div class="data-label">' + item.label + ':</div>';
                html += '<div class="data-value">' + item.value + '</div>';
                html += '<div class="data-explanation">' + item.explanation + '</div>';
                html += '</div>';
            });
            
            html += '</div>';
            return html;
        }
        
        // Enhanced client-side data collection
        function getWebGLFingerprint() {
            try {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (!gl) return 'Not supported';
                
                const renderer = gl.getParameter(gl.RENDERER);
                const vendor = gl.getParameter(gl.VENDOR);
                return `${vendor} - ${renderer}`.slice(0, 50);
            } catch (e) {
                return 'Error getting WebGL info';
            }
        }
        
        function getCanvasFingerprint() {
            try {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                ctx.textBaseline = 'top';
                ctx.font = '14px Arial';
                ctx.fillText('Privacy Demo 🔍', 2, 2);
                return canvas.toDataURL().slice(-20);
            } catch (e) {
                return 'Error generating canvas fingerprint';
            }
        }
        
        function getAllCookies() {
            const cookies = {};
            if (document.cookie) {
                document.cookie.split(';').forEach(cookie => {
                    const [name, value] = cookie.trim().split('=');
                    if (name) cookies[name] = value || '';
                });
            }
            return cookies;
        }
        
        function getStorageInfo() {
            const storage = {
                localStorage: false,
                sessionStorage: false,
                localStorageData: {},
                sessionStorageData: {}
            };
            
            try {
                localStorage.setItem('test', 'test');
                localStorage.removeItem('test');
                storage.localStorage = true;
            } catch (e) {
                storage.localStorage = false;
            }
            
            try {
                sessionStorage.setItem('test', 'test');
                sessionStorage.removeItem('test');
                storage.sessionStorage = true;
            } catch (e) {
                storage.sessionStorage = false;
            }
            
            return storage;
        }
        
        // Store comprehensive client data on page load
        window.onload = function() {
            window.clientInfo = {
                screen_width: screen.width,
                screen_height: screen.height,
                screen_colorDepth: screen.colorDepth,
                window_width: window.innerWidth,
                window_height: window.innerHeight,
                device_pixel_ratio: window.devicePixelRatio || 1,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                locale: Intl.DateTimeFormat().resolvedOptions().locale,
                storage_info: getStorageInfo(),
                canvas_fingerprint: getCanvasFingerprint(),
                webgl_fingerprint: getWebGLFingerprint(),
                cookies: getAllCookies(),
                java_enabled: navigator.javaEnabled ? navigator.javaEnabled() : false,
                plugins: Array.from(navigator.plugins || []).map(p => ({
                    name: p.name,
                    description: p.description
                })),
                navigator_info: {
                    platform: navigator.platform,
                    language: navigator.language,
                    languages: navigator.languages || [],
                    vendor: navigator.vendor || 'Unknown',
                    cookieEnabled: navigator.cookieEnabled,
                    onLine: navigator.onLine,
                    doNotTrack: navigator.doNotTrack,
                    hardwareConcurrency: navigator.hardwareConcurrency || 'Unknown',
                    maxTouchPoints: navigator.maxTouchPoints || 0
                }
            };
        };
    </script>
</body>
</html>
"""

def get_ip_location(ip_address):
    """Get location information from IP address using ipapi.co (free service)"""
    try:
        # Skip local/private IPs
        if ip_address.startswith(('127.', '192.168.', '10.', '172.')):
            return {
                'city': 'Local Network',
                'region': 'Private IP',
                'country': 'Local',
                'isp': 'Local Network',
                'accuracy': 'N/A - Private IP'
            }
        
        response = requests.get(f'http://ipapi.co/{ip_address}/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'city': data.get('city', 'Unknown'),
                'region': data.get('region', 'Unknown'),
                'country': data.get('country_name', 'Unknown'),
                'isp': data.get('org', 'Unknown ISP'),
                'accuracy': '~1-50 km radius'
            }
    except Exception as e:
        print(f"Location lookup failed: {e}")
    
    return {
        'city': 'Lookup Failed',
        'region': 'Unknown',
        'country': 'Unknown',
        'isp': 'Unknown',
        'accuracy': 'N/A'
    }

def parse_user_agent(user_agent):
    """Extract OS and browser info from user agent string"""
    os_info = "Unknown OS"
    browser_info = "Unknown Browser"
    
    # Simple OS detection
    if "Windows NT 10" in user_agent:
        os_info = "Windows 10/11"
    elif "Windows NT" in user_agent:
        os_info = "Windows (older version)"
    elif "Mac OS X" in user_agent or "macOS" in user_agent:
        os_info = "macOS"
    elif "Linux" in user_agent:
        os_info = "Linux"
    elif "Android" in user_agent:
        os_info = "Android"
    elif "iPhone" in user_agent or "iPad" in user_agent:
        os_info = "iOS"
    
    # Simple browser detection
    if "Chrome" in user_agent and "Edge" not in user_agent and "OPR" not in user_agent:
        browser_info = "Google Chrome"
    elif "Edge" in user_agent:
        browser_info = "Microsoft Edge"
    elif "Firefox" in user_agent:
        browser_info = "Mozilla Firefox"
    elif "Safari" in user_agent and "Chrome" not in user_agent:
        browser_info = "Safari"
    elif "OPR" in user_agent:
        browser_info = "Opera"
    
    return os_info, browser_info

def calculate_privacy_score(request):
    """Calculate a privacy score based on request characteristics"""
    score = 100  # Start with perfect privacy score
    
    # Deduct points for tracking indicators
    if request.headers.get('DNT') != '1':
        score -= 10  # No Do Not Track header
    
    if len(request.cookies) > 0:
        score -= min(len(request.cookies) * 5, 30)  # Cookies present
    
    if request.headers.get('Referer'):
        score -= 5  # Referer header reveals browsing history
    
    # Check for tracking cookies
    tracking_cookies = ['ga', 'fb', 'track', 'analytics', '_utm', 'doubleclick']
    if request.cookies and any(tracker in k.lower() for k in request.cookies.keys() for tracker in tracking_cookies):
        score -= 20  # Tracking cookies present
    
    # Check for fingerprinting headers
    if request.headers.get('Sec-CH-UA'):
        score -= 5  # Client Hints can be used for fingerprinting
    
    return max(score, 0)  # Don't go below 0

def assess_tracking_risk(request):
    """Assess the tracking risk level"""
    risk_factors = []
    
    if len(request.cookies) > 5:
        risk_factors.append("Many cookies present")
    
    if request.headers.get('Referer'):
        risk_factors.append("Referer header exposes browsing history")
    
    tracking_cookies = ['ga', 'fb', 'track', 'analytics', '_utm']
    if request.cookies and any(tracker in k.lower() for k in request.cookies.keys() for tracker in tracking_cookies):
        risk_factors.append("Tracking cookies detected")
    
    if not request.headers.get('DNT'):
        risk_factors.append("No Do Not Track preference set")
    
    if request.headers.get('Sec-CH-UA'):
        risk_factors.append("Browser fingerprinting headers present")
    
    if len(risk_factors) == 0:
        return {"level": "LOW", "factors": ["Good privacy protection detected"]}
    elif len(risk_factors) <= 2:
        return {"level": "MEDIUM", "factors": risk_factors}
    else:
        return {"level": "HIGH", "factors": risk_factors}

@app.route('/')
def demo_page():
    """Serve the demonstration page"""
    return render_template_string(DEMO_PAGE)

def calculate_fingerprint_resistance(request, client_data):
    """Calculate how resistant the user's setup is to fingerprinting"""
    resistance_score = 100
    resistance_factors = []
    
    # Check User Agent
    user_agent = request.headers.get('User-Agent', '')
    if 'Chrome' in user_agent and 'Safari' in user_agent:
        resistance_score -= 15
        resistance_factors.append("Common Chrome/Safari user agent (easily fingerprintable)")
    
    # Check if using Tor or privacy browser
    if 'Tor' in user_agent:
        resistance_score += 20
        resistance_factors.append("Using Tor Browser (good fingerprint resistance)")
    elif 'Firefox' in user_agent and 'rv:' in user_agent:
        resistance_score += 5
        resistance_factors.append("Using Firefox (better privacy than Chrome)")
    
    # Check canvas fingerprinting availability
    if client_data.get('canvas_fingerprint') and client_data.get('canvas_fingerprint') != 'Not available':
        resistance_score -= 20
        resistance_factors.append("Canvas fingerprinting enabled (major privacy risk)")
    
    # Check WebGL fingerprinting
    if client_data.get('webgl_fingerprint') and client_data.get('webgl_fingerprint') != 'Not available':
        resistance_score -= 20
        resistance_factors.append("WebGL fingerprinting enabled (major privacy risk)")
    
    # Check for Do Not Track
    if request.headers.get('DNT') == '1':
        resistance_score += 5
        resistance_factors.append("Do Not Track enabled (limited but positive)")
    
    # Check plugins
    plugin_count = len(client_data.get('plugins', []))
    if plugin_count > 5:
        resistance_score -= 10
        resistance_factors.append(f"Many plugins detected ({plugin_count}) - increases fingerprint uniqueness")
    elif plugin_count == 0:
        resistance_score += 5
        resistance_factors.append("No plugins detected (reduces fingerprint surface)")
    
    # Check screen resolution uniqueness
    screen_width = client_data.get('screen_width', 0)
    screen_height = client_data.get('screen_height', 0)
    common_resolutions = [(1920, 1080), (1366, 768), (1440, 900), (1280, 720), (1024, 768)]
    if (screen_width, screen_height) not in common_resolutions and screen_width > 0:
        resistance_score -= 15
        resistance_factors.append(f"Uncommon screen resolution ({screen_width}x{screen_height}) - highly identifiable")
    
    # Check timezone
    timezone = client_data.get('timezone', '')
    common_timezones = ['America/New_York', 'America/Los_Angeles', 'Europe/London', 'Europe/Berlin']
    if timezone and timezone not in common_timezones:
        resistance_score -= 5
        resistance_factors.append("Uncommon timezone increases fingerprint uniqueness")
    
    # Ensure score is within bounds
    resistance_score = max(0, min(100, resistance_score))
    
    return {
        'score': resistance_score,
        'level': 'HIGH' if resistance_score > 70 else 'MEDIUM' if resistance_score > 40 else 'LOW',
        'factors': resistance_factors
    }

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_request():
    """Analyze the request and return comprehensive data exposure information with explanations"""
    # Get client IP (handle proxies/load balancers)
    client_ip = request.headers.get('X-Forwarded-For', 
                request.headers.get('X-Real-IP', 
                request.remote_addr)).split(',')[0].strip()
    
    # Get location data
    location_data = get_ip_location(client_ip)
    
    # Parse user agent
    user_agent = request.headers.get('User-Agent', 'Unknown')
    os_info, browser_info = parse_user_agent(user_agent)
    
    # Get client-side data
    client_data = request.get_json() or {}
    
    # Collect comprehensive data with explanations
    exposure_data = {
        # Network Information with explanations
        'ip_address': client_ip,
        'ip_explanation': 'Your unique internet address that websites use to send data back to you. This can reveal your approximate location and internet provider.',
        
        'location': f"{location_data['city']}, {location_data['region']}, {location_data['country']}",
        'location_explanation': 'Your approximate physical location based on your IP address. Accurate within 1-50km radius.',
        
        'isp': location_data['isp'],
        'isp_explanation': 'Your Internet Service Provider - the company you pay for internet access. This can reveal your general area and connection type.',
        
        'connection_type': 'Broadband/Mobile' if not client_ip.startswith(('127.', '192.168.')) else 'Local',
        'connection_explanation': 'The type of internet connection you\'re using (WiFi, mobile data, wired, etc.).',
        
        'real_ip': request.headers.get('X-Real-IP', 'Not found'),
        'forwarded_for': request.headers.get('X-Forwarded-For', 'Not found'),
        'cloudflare_ip': request.headers.get('CF-Connecting-IP', 'Not found'),
        
        # Device & Browser Information with explanations
        'os_info': os_info,
        'os_explanation': 'Your operating system (Windows, Mac, iPhone, etc.). This helps websites optimize content for your device.',
        
        'browser': browser_info,
        'browser_explanation': 'Your web browser software. Different browsers have different capabilities and security features.',
        
        'user_agent': user_agent,
        'user_agent_explanation': 'A detailed string that identifies your browser, operating system, and device. This is like a digital fingerprint.',
        
        'language': request.headers.get('Accept-Language', 'Unknown').split(',')[0],
        'language_explanation': 'Your preferred language settings. This can reveal your geographic region and cultural background.',
        
        'do_not_track': request.headers.get('DNT', 'Not set'),
        'dnt_explanation': 'A setting that tells websites you don\'t want to be tracked. However, websites can ignore this preference.',
        
        'upgrade_insecure_requests': request.headers.get('Upgrade-Insecure-Requests', 'Not set'),
        
        # Screen and Device Details (from client-side) with explanations
        'screen_info': f"{client_data.get('screen_width', 'Unknown')} x {client_data.get('screen_height', 'Unknown')} pixels",
        'screen_explanation': 'Your screen resolution. This helps create a unique fingerprint of your device and can reveal your device type.',
        
        'timezone': client_data.get('timezone', 'Unknown'),
        'timezone_explanation': 'Your time zone setting. This can reveal your geographic location and daily patterns.',
        
        'device_pixel_ratio': client_data.get('device_pixel_ratio', 'Unknown'),
        'pixel_ratio_explanation': 'How your device displays pixels. High-DPI displays have different ratios, helping identify device types.',
        
        # HTTP Headers (Security & Tracking) with explanations
        'referer': request.headers.get('Referer', 'Direct visit'),
        'referer_explanation': 'The website you came from before visiting this page. This reveals your browsing history to websites.',
        
        'origin': request.headers.get('Origin', 'Not set'),
        'origin_explanation': 'The website that initiated this request. Used for security but can reveal your browsing patterns.',
        
        'accept_language': request.headers.get('Accept-Language', 'Unknown'),
        'accept_encoding': request.headers.get('Accept-Encoding', 'Unknown'),
        'accept': request.headers.get('Accept', 'Unknown'),
        'connection': request.headers.get('Connection', 'Unknown'),
        'cache_control': request.headers.get('Cache-Control', 'Not set'),
        'pragma': request.headers.get('Pragma', 'Not set'),
        'sec_fetch_site': request.headers.get('Sec-Fetch-Site', 'Not set'),
        'sec_fetch_mode': request.headers.get('Sec-Fetch-Mode', 'Not set'),
        'sec_fetch_user': request.headers.get('Sec-Fetch-User', 'Not set'),
        'sec_fetch_dest': request.headers.get('Sec-Fetch-Dest', 'Not set'),
        'sec_fetch_explanation': 'Security headers that browsers send to protect against attacks, but also provide fingerprinting data.',
        
        'sec_ch_ua': request.headers.get('Sec-CH-UA', 'Not available'),
        'sec_ch_ua_mobile': request.headers.get('Sec-CH-UA-Mobile', 'Not available'),
        'sec_ch_ua_platform': request.headers.get('Sec-CH-UA-Platform', 'Not available'),
        
        # Cookies & Session Data with explanations
        'cookies': dict(request.cookies) if request.cookies else {},
        'cookie_count': len(request.cookies) if request.cookies else 0,
        'cookie_explanation': 'Small files stored on your device that remember information about you. These can track your visits across websites.',
        
        'has_session_cookies': any('session' in k.lower() for k in request.cookies.keys()) if request.cookies else False,
        'session_explanation': 'Temporary cookies that remember you during your current browsing session.',
        
        'has_tracking_cookies': any(tracker in k.lower() for k in request.cookies.keys() for tracker in ['ga', 'fb', 'track', 'analytics', '_utm']) if request.cookies else False,
        'tracking_explanation': 'Cookies used by advertising companies to follow you across different websites and build profiles.',
        
        # Browser Fingerprinting with comprehensive explanations
        'session_id': hashlib.md5((client_ip + user_agent).encode()).hexdigest()[:12],
        'session_explanation': 'A unique identifier created for your current visit. This can be used to track your actions on the website.',
        
        'unique_fingerprint': hashlib.sha256((client_ip + user_agent + str(request.headers.get('Accept-Language', ''))).encode()).hexdigest()[:16],
        'fingerprint_explanation': 'A digital signature created from your browser and device characteristics. Like a real fingerprint, this is unique to you and can identify you across different websites even without cookies.',
        
        'canvas_fingerprint': client_data.get('canvas_fingerprint', 'Not available'),
        'canvas_explanation': 'Your graphics card and drivers render text/images slightly differently than others. This creates a unique "canvas fingerprint" that\'s highly stable and can track you across incognito sessions and different browsers.',
        
        'webgl_fingerprint': client_data.get('webgl_fingerprint', 'Not available'),
        'webgl_explanation': 'Information about your graphics processing unit (GPU). Different graphics cards have unique capabilities and render 3D graphics differently, creating another highly accurate tracking method.',
        
        # Additional fingerprinting methods
        'screen_fingerprint': f"{client_data.get('screen_width', 'Unknown')}x{client_data.get('screen_height', 'Unknown')}@{client_data.get('screen_colorDepth', 'Unknown')}bit",
        'screen_explanation': 'Your exact screen resolution and color depth. While many people share common resolutions (1920x1080), the combination with other factors makes you more identifiable.',
        
        'timezone_fingerprint': client_data.get('timezone', 'Unknown'),
        'timezone_explanation': 'Your timezone setting reveals your geographic location and can be combined with other data to create a more accurate fingerprint.',
        
        'language_fingerprint': request.headers.get('Accept-Language', 'Unknown'),
        'language_explanation': 'Your language preferences create a fingerprint. The specific order of languages you prefer is often unique to you.',
        
        'plugin_fingerprint': str(len(client_data.get('plugins', []))),
        'plugin_explanation': 'The number and types of browser plugins you have installed. Each person has a unique combination of plugins (PDF viewers, extensions, etc.) that can identify them.',
        
        'font_detection': 'Possible via CSS/JS',
        'font_explanation': 'Websites can detect which fonts are installed on your computer. Your unique collection of fonts (from software you\'ve installed) creates another fingerprint dimension.',
        
        'audio_fingerprint': 'Detectable via AudioContext API',
        'audio_explanation': 'Your device\'s audio hardware processes sounds slightly differently. Websites can measure these tiny differences to create an "audio fingerprint" unique to your device.',
        
        'battery_fingerprint': 'Available via Battery API',
        'battery_explanation': 'Some browsers expose battery level and charging status. This information changes over time but can be used for short-term tracking.',
        
        'fingerprint_resistance': calculate_fingerprint_resistance(request, client_data),
        'resistance_explanation': 'How well your browser setup resists fingerprinting. Higher resistance means you\'re harder to track uniquely.',
        
        'fingerprint_persistence': 'Survives: cookie deletion, incognito mode, some VPNs',
        'persistence_explanation': 'Unlike cookies, browser fingerprints cannot be easily deleted. They work in incognito mode and even when using some VPNs, making them a powerful tracking method.',
        
        # Storage Capabilities with explanations
        'storage_info': client_data.get('storage_info', {}),
        'storage_explanation': 'What types of data storage your browser supports. Websites can use these to store tracking information.',
        
        # Hardware Information with explanations
        'hardware_info': client_data.get('navigator_info', {}).get('hardwareConcurrency', 'Unknown'),
        'hardware_explanation': 'Information about your device\'s processing power. This helps create a unique device fingerprint.',
        
        'plugins': client_data.get('plugins', []),
        'plugins_explanation': 'Software extensions installed in your browser. The combination of plugins can uniquely identify you.',
        
        # Request Details
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'method': request.method,
        'url': request.url,
        'full_path': request.full_path,
        'endpoint': request.endpoint,
        'remote_addr': request.remote_addr,
        'scheme': request.scheme,
        'host': request.host,
        'is_secure': request.is_secure,
        'content_length': request.content_length,
        'content_type': request.content_type,
        
        # Form/Query Data (if any)
        'query_params': dict(request.args) if request.args else {},
        'form_data': dict(request.form) if request.form else {},
        'json_data': client_data,
        
        # All HTTP Headers (for educational purposes)
        'all_headers': dict(request.headers),
        'header_count': len(request.headers),
        
        # Privacy Assessment with explanations
        'privacy_score': calculate_privacy_score(request),
        'score_explanation': 'Your privacy protection level (0-100). Lower scores mean you\'re easier to track and profile.',
        
        'tracking_risk': assess_tracking_risk(request),
        'risk_explanation': 'Assessment of how easily companies can track and profile you based on the data you\'re sharing.',
        
        # Complete technical data for advanced users
        'technical_data': {
            'all_headers': dict(request.headers),
            'request_details': {
                'method': request.method,
                'url': request.url,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
                'is_secure': request.is_secure
            }
        }
    }
    
    return jsonify(exposure_data)

@app.route('/set-demo-cookies')
def set_demo_cookies():
    """Set some demonstration cookies to show how tracking works"""
    response = make_response(jsonify({
        'message': 'Demo cookies have been set!',
        'cookies_set': [
            'session_id: Unique session identifier',
            'user_prefs: User preferences',
            'analytics_ga: Google Analytics tracking',
            'fb_pixel: Facebook tracking pixel',
            'utm_source: Marketing campaign tracking'
        ]
    }))
    
    # Set various types of cookies
    response.set_cookie('demo_session_id', 'sess_' + hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12])
    response.set_cookie('demo_user_prefs', 'theme=dark&lang=en')
    response.set_cookie('demo_analytics_ga', 'GA1.2.123456789.1234567890')
    response.set_cookie('demo_fb_pixel', 'fb.1.1234567890123.1234567890')
    response.set_cookie('demo_utm_source', 'privacy_demo')
    response.set_cookie('demo_tracking', 'track_' + hashlib.md5(request.remote_addr.encode()).hexdigest()[:8])
    
    return response

@app.route('/clear-cookies')
def clear_cookies():
    """Clear demonstration cookies"""
    response = make_response(jsonify({
        'message': 'Demo cookies have been cleared!',
        'note': 'Refresh the page and run the analysis again to see the difference'
    }))
    
    # Clear the demo cookies
    cookie_names = ['demo_session_id', 'demo_user_prefs', 'demo_analytics_ga', 'demo_fb_pixel', 'demo_utm_source', 'demo_tracking']
    for cookie_name in cookie_names:
        response.set_cookie(cookie_name, '', expires=0)
    
    return response

@app.route('/fingerprint-test')
def fingerprint_test():
    """Show detailed browser fingerprinting data"""
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    fingerprint_data = {
        'browser_fingerprint': {
            'user_agent_hash': hashlib.sha256(user_agent.encode()).hexdigest()[:16],
            'header_fingerprint': hashlib.sha256(str(sorted(request.headers.items())).encode()).hexdigest()[:16],
            'ip_hash': hashlib.sha256(request.remote_addr.encode()).hexdigest()[:16],
        },
        'uniqueness_score': 'Very High - you can be tracked across websites',
        'explanation': 'Even without cookies, your browser fingerprint is likely unique among millions of users',
        'mitigation': 'Use Tor Browser, Firefox with privacy.resistFingerprinting=true, or a browser with fingerprint protection'
    }
    
    return jsonify(fingerprint_data)

@app.route('/privacy-tips')
def privacy_tips():
    """Enhanced endpoint with comprehensive privacy protection tips"""
    tips = {
        'immediate_actions': [
            'Use a VPN service to hide your IP address and location',
            'Install uBlock Origin or similar ad blocker to block trackers',
            'Use Firefox with strict privacy settings or consider Tor Browser',
            'Regularly clear cookies, browsing history, and cached data',
            'Disable location services for browsers',
            'Enable "Do Not Track" in browser settings',
            'Disable third-party cookies in browser settings'
        ],
        'browser_settings': [
            'Firefox: Set privacy.resistFingerprinting = true in about:config',
            'Chrome: Use guest mode or create separate profiles for different activities',
            'Safari: Enable "Prevent cross-site tracking" in preferences',
            'Edge: Enable "Prevent tracking" in privacy settings',
            'Use private/incognito browsing mode for sensitive activities',
            'Install privacy-focused browser extensions (Ghostery, Privacy Badger)',
            'Consider using multiple browsers for different purposes'
        ],
        'advanced_protection': [
            'Use a privacy-focused DNS service (1.1.1.1, 9.9.9.9, or Quad9)',
            'Enable HTTPS Everywhere or similar extension',
            'Use different browsers for different activities (work, personal, shopping)',
            'Consider using virtual machines for isolation',
            'Review and adjust social media privacy settings regularly',
            'Use disposable email addresses for online accounts',
            'Enable two-factor authentication where possible'
        ],
        'mobile_protection': [
            'Disable app tracking on iOS/Android',
            'Use privacy-focused mobile browsers (Firefox Focus, DuckDuckGo)',
            'Regularly review app permissions',
            'Use VPN on mobile devices',
            'Disable advertising ID sharing',
            'Turn off location history and web activity tracking'
        ],
        'data_explanation': {
            'why_companies_want_data': 'Companies collect this data to build detailed profiles for targeted advertising, price discrimination, and to sell to data brokers. Your data is extremely valuable.',
            'tracking_methods': 'Beyond cookies, companies use browser fingerprinting, pixel tracking, device fingerprinting, and cross-device tracking to follow you.',
            'privacy_laws': 'GDPR in Europe and CCPA in California give you rights to know what data is collected and to delete it. Use these rights.',
            'long_term_risks': 'Data breaches can expose your information years later. Insurance companies and employers may use this data against you.'
        }
    }
    
    return jsonify(tips)

def print_startup_info():
    """Print startup information for facilitators"""
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = '127.0.1.1'
    
    print("🔍" * 30)
    print("   DATA EXPOSURE REVEALED - ENHANCED PRIVACY EDUCATION")
    print("🔍" * 30)
    print(f"\n🌐 Server running on:")
    print(f"   Local:    http://localhost:5000")
    print(f"   Network:  http://{local_ip}:5000")
    print(f"\n📋 FACILITATOR INSTRUCTIONS:")
    print(f"   1. Share the network URL with participants")
    print(f"   2. Have them visit the page on their devices")
    print(f"   3. Ask them to click 'REVEAL WHAT WEBSITES KNOW ABOUT ME'")
    print(f"   4. Try the cookie demo and fingerprint test")
    print(f"   5. Discuss each section and its privacy implications")
    print(f"   6. Review the protection tips provided")
    print(f"   7. Use /privacy-tips endpoint for comprehensive solutions")
    print(f"\n🆕 NEW FEATURES IN REVEALED EDITION:")
    print(f"   • Detailed explanations for every piece of data collected")
    print(f"   • Clear privacy implications and risks")
    print(f"   • Actionable protection advice")
    print(f"   • Enhanced visual presentation")
    print(f"   • Mobile-friendly responsive design")
    print(f"   • Advanced fingerprinting demonstration")
    print(f"\n💡 DISCUSSION POINTS:")
    print(f"   • How much can websites learn about you without asking?")
    print(f"   • Why is this data valuable to companies and advertisers?")
    print(f"   • What are the long-term privacy and security risks?")
    print(f"   • How can individuals and organizations protect privacy?")
    print(f"   • What legal rights do users have regarding their data?")
    print(f"\n🎯 Learning Objective: Complete digital privacy literacy")
    print("🔍" * 30)

if __name__ == '__main__':
    print_startup_info()
    
    # Run the Flask application
    # Use 0.0.0.0 to allow network access from other devices
    app.run(host='0.0.0.0', port=5000, debug=True)
