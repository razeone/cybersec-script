#!/usr/bin/env python3
"""
🕵️ HTTP REQUEST DATA EXPOSURE DEMONSTRATION
Shows participants exactly what data they reveal with every web request
Perfect for cybersecurity awareness training!
"""

from flask import Flask, request, jsonify, render_template_string
import socket
import json
from datetime import datetime
import os
import requests
import hashlib

app = Flask(__name__)

# HTML template for the demo page
DEMO_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>🔍 Data Exposure Demo - Click to See What You Share!</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
            print(f"🎯 Learning Objective: Awareness of digital footprint")
    print("🕵️" * 30)

@app.route('/set-demo-cookies')
def set_demo_cookies():
    """Set some demonstration cookies to show how tracking works"""
    from flask import make_response
    
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
    from flask import make_response
    
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

if __name__ == '__main__': { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 { text-align: center; font-size: 2.5em; margin-bottom: 30px; }
        .warning { 
            background: #ff6b6b; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
        }
        .demo-button {
            background: #4ecdc4;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.2em;
            border-radius: 8px;
            cursor: pointer;
            display: block;
            margin: 30px auto;
            transition: all 0.3s;
        }
        .demo-button:hover {
            background: #45b7b8;
            transform: translateY(-2px);
        }
        .results {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            font-family: monospace;
            white-space: pre-wrap;
            display: none;
        }
        .scary { color: #ff6b6b; font-weight: bold; }
        .info { color: #4ecdc4; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🕵️ What Data Are You Sharing Right Now?</h1>
        
        <div class="warning">
            ⚠️ WARNING: This demo will show you REAL data about your device and connection!
        </div>
        
        <p style="text-align: center; font-size: 1.1em;">
            Every time you visit a website, you automatically share information about yourself.<br>
            <strong>Click the button below to see exactly what data you're revealing right now!</strong>
        </p>
        
        <button class="demo-button" onclick="revealData()">
            🔍 REVEAL MY DATA EXPOSURE
        </button>
        
        <div id="results" class="results"></div>
        
        <div style="margin-top: 30px; font-size: 0.9em; text-align: center; opacity: 0.8;">
            <p>💡 This demonstration is for educational purposes only.<br>
            No data is stored or shared with third parties.</p>
        </div>
    </div>

    <script>
        function revealData() {
            document.getElementById('results').style.display = 'block';
            document.getElementById('results').innerHTML = '🔄 Analyzing your digital footprint...';
            
            fetch('/analyze')
                .then(response => response.json())
                .then(data => {
                    displayResults(data);
                })
                .catch(error => {
                    document.getElementById('results').innerHTML = 'Error: ' + error;
                });
        }
        
        function displayResults(data) {
            let html = `
<span class="scary">🚨 YOUR DIGITAL FOOTPRINT REVEALED 🚨</span>

<span class="info">📍 LOCATION INFORMATION:</span>
Your IP Address: <span class="scary">${data.ip_address}</span>
Estimated Location: <span class="scary">${data.location}</span>
Internet Provider: <span class="scary">${data.isp}</span>
Connection Type: ${data.connection_type}

<span class="info">🖥️ DEVICE & BROWSER FINGERPRINT:</span>
Operating System: <span class="scary">${data.os_info}</span>
Browser: <span class="scary">${data.browser}</span>
Screen Resolution: ${data.screen_info}
Language Settings: ${data.language}
Time Zone: <span class="scary">${data.timezone}</span>

<span class="info">🌐 NETWORK DETAILS:</span>
User Agent: ${data.user_agent}
Referer: ${data.referer || 'Direct visit'}
Accept Languages: ${data.accept_language}
Accept Encoding: ${data.accept_encoding}

<span class="info">🕒 SESSION INFORMATION:</span>
Request Timestamp: ${data.timestamp}
Session Fingerprint: ${data.session_id}

<span class="info">🔍 TRACKING CAPABILITIES:</span>
Cookies Enabled: <span class="scary">${data.cookies_enabled}</span>
JavaScript Enabled: <span class="scary">Yes (obviously!)</span>
Local Storage Available: <span class="scary">${data.local_storage}</span>
Canvas Fingerprinting: <span class="scary">${data.canvas_fingerprint}</span>

<span class="scary">⚠️ PRIVACY IMPLICATIONS:</span>
• Websites can track your location within ${data.location_accuracy}
• Your device can be uniquely identified across websites
• Your browsing patterns can be correlated and profiled
• Third-party trackers can build a detailed profile about you
• This data can be sold to advertisers and data brokers

<span class="info">🛡️ WHAT CAN YOU DO?</span>
✅ Use a VPN to hide your real IP address
✅ Use privacy-focused browsers (Firefox with strict settings)
✅ Install ad blockers and tracking protection
✅ Regularly clear cookies and browser data
✅ Use Tor browser for sensitive browsing
✅ Disable location services when not needed
`;
            document.getElementById('results').innerHTML = html;
        }
        
        // Check if local storage is available
        function checkLocalStorage() {
            try {
                localStorage.setItem('test', 'test');
                localStorage.removeItem('test');
                return 'Available';
            } catch(e) {
                return 'Blocked/Unavailable';
            }
        }
        
        // Create a simple canvas fingerprint
        function getCanvasFingerprint() {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillText('Privacy Demo 🔍', 2, 2);
            return canvas.toDataURL().slice(-20);
        }
        
        // Get WebGL fingerprint
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
        
        // Get available fonts (fingerprinting technique)
        function getFontFingerprint() {
            const testFonts = ['Arial', 'Times', 'Courier', 'Helvetica', 'Verdana', 'Georgia', 'Impact'];
            const availableFonts = [];
            
            testFonts.forEach(font => {
                const testElement = document.createElement('span');
                testElement.style.fontFamily = font;
                testElement.style.fontSize = '72px';
                testElement.innerHTML = 'mmmmmmmmmmlli';
                testElement.style.position = 'absolute';
                testElement.style.left = '-9999px';
                document.body.appendChild(testElement);
                
                const width = testElement.offsetWidth;
                document.body.removeChild(testElement);
                
                if (width > 0) availableFonts.push(font);
            });
            
            return availableFonts.join(',');
        }
        
        // Get audio fingerprint
        function getAudioFingerprint() {
            try {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const analyser = audioContext.createAnalyser();
                const gainNode = audioContext.createGain();
                const scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
                
                oscillator.connect(analyser);
                analyser.connect(scriptProcessor);
                scriptProcessor.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                return `${audioContext.sampleRate}-${audioContext.baseLatency || 'unknown'}`;
            } catch (e) {
                return 'Audio context not available';
            }
        }
        
        // Get all available cookies
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
        
        // Test local storage and session storage
        function getStorageInfo() {
            const storage = {
                localStorage: false,
                sessionStorage: false,
                indexedDB: false,
                webSQL: false,
                localStorageData: {},
                sessionStorageData: {}
            };
            
            try {
                localStorage.setItem('test', 'test');
                localStorage.removeItem('test');
                storage.localStorage = true;
                
                // Get existing localStorage data (for demo purposes)
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    storage.localStorageData[key] = localStorage.getItem(key)?.slice(0, 50) + '...';
                }
            } catch (e) {
                storage.localStorage = false;
            }
            
            try {
                sessionStorage.setItem('test', 'test');
                sessionStorage.removeItem('test');
                storage.sessionStorage = true;
                
                // Get existing sessionStorage data (for demo purposes)
                for (let i = 0; i < sessionStorage.length; i++) {
                    const key = sessionStorage.key(i);
                    storage.sessionStorageData[key] = sessionStorage.getItem(key)?.slice(0, 50) + '...';
                }
            } catch (e) {
                storage.sessionStorage = false;
            }
            
            storage.indexedDB = !!window.indexedDB;
            storage.webSQL = !!window.openDatabase;
            
            return storage;
        }
        
        // Get detailed navigator information
        function getNavigatorInfo() {
            return {
                platform: navigator.platform,
                language: navigator.language,
                languages: navigator.languages || [],
                userAgent: navigator.userAgent,
                vendor: navigator.vendor || 'Unknown',
                cookieEnabled: navigator.cookieEnabled,
                onLine: navigator.onLine,
                doNotTrack: navigator.doNotTrack,
                hardwareConcurrency: navigator.hardwareConcurrency || 'Unknown',
                maxTouchPoints: navigator.maxTouchPoints || 0,
                deviceMemory: navigator.deviceMemory || 'Unknown',
                connection: navigator.connection ? {
                    effectiveType: navigator.connection.effectiveType,
                    downlink: navigator.connection.downlink,
                    rtt: navigator.connection.rtt
                } : 'Not available'
            };
        }
        
        // Add additional client-side data collection
        window.onload = function() {
            // Store comprehensive client-side info
            window.clientInfo = {
                // Basic screen info
                screen_width: screen.width,
                screen_height: screen.height,
                screen_colorDepth: screen.colorDepth,
                screen_pixelDepth: screen.pixelDepth,
                
                // Window and viewport info
                window_width: window.innerWidth,
                window_height: window.innerHeight,
                device_pixel_ratio: window.devicePixelRatio || 1,
                
                // Time and location
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                locale: Intl.DateTimeFormat().resolvedOptions().locale,
                
                // Storage capabilities
                storage_info: getStorageInfo(),
                
                // Fingerprinting data
                canvas_fingerprint: getCanvasFingerprint(),
                webgl_fingerprint: getWebGLFingerprint(),
                audio_fingerprint: getAudioFingerprint(),
                font_fingerprint: getFontFingerprint(),
                
                // Navigator details
                navigator_info: getNavigatorInfo(),
                
                // Cookies
                cookies: getAllCookies(),
                
                // Additional capabilities
                java_enabled: navigator.javaEnabled ? navigator.javaEnabled() : false,
                plugins: Array.from(navigator.plugins || []).map(p => ({
                    name: p.name,
                    description: p.description,
                    version: p.version
                })),
                
                // Performance info
                performance_timing: performance.timing ? {
                    navigationStart: performance.timing.navigationStart,
                    loadEventEnd: performance.timing.loadEventEnd,
                    domContentLoadedEventEnd: performance.timing.domContentLoadedEventEnd
                } : 'Not available'
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

@app.route('/analyze')
def analyze_request():
    """Analyze and return all available request data"""
    
    # Get client IP address (handle proxy scenarios)
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()
    
    # Get location data
    location_data = get_ip_location(client_ip)
    
    # Parse user agent
    user_agent = request.headers.get('User-Agent', 'Unknown')
    os_info, browser_info = parse_user_agent(user_agent)
    
    # Collect all available data
    exposure_data = {
        # Network Information
        'ip_address': client_ip,
        'location': f"{location_data['city']}, {location_data['region']}, {location_data['country']}",
        'isp': location_data['isp'],
        'location_accuracy': location_data['accuracy'],
        'connection_type': 'Broadband/Mobile' if not client_ip.startswith(('127.', '192.168.')) else 'Local',
        'real_ip': request.headers.get('X-Real-IP', 'Not found'),
        'forwarded_for': request.headers.get('X-Forwarded-For', 'Not found'),
        'cloudflare_ip': request.headers.get('CF-Connecting-IP', 'Not found'),
        
        # Device & Browser Fingerprint
        'os_info': os_info,
        'browser': browser_info,
        'user_agent': user_agent,
        'screen_info': 'Detected via JavaScript',
        'language': request.headers.get('Accept-Language', 'Unknown').split(',')[0],
        'timezone': 'Detected via JavaScript',
        'do_not_track': request.headers.get('DNT', 'Not set'),
        'upgrade_insecure_requests': request.headers.get('Upgrade-Insecure-Requests', 'Not set'),
        
        # HTTP Headers (Security & Tracking)
        'referer': request.headers.get('Referer', 'Direct visit'),
        'origin': request.headers.get('Origin', 'Not set'),
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
        'sec_ch_ua': request.headers.get('Sec-CH-UA', 'Not available'),
        'sec_ch_ua_mobile': request.headers.get('Sec-CH-UA-Mobile', 'Not available'),
        'sec_ch_ua_platform': request.headers.get('Sec-CH-UA-Platform', 'Not available'),
        
        # Cookies & Session Data
        'cookies': dict(request.cookies) if request.cookies else {},
        'cookie_count': len(request.cookies) if request.cookies else 0,
        'has_session_cookies': any('session' in k.lower() for k in request.cookies.keys()) if request.cookies else False,
        'has_tracking_cookies': any(tracker in k.lower() for k in request.cookies.keys() for tracker in ['ga', 'fb', 'track', 'analytics', '_utm']) if request.cookies else False,
        
        # Session & Tracking
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'session_id': hashlib.md5((client_ip + user_agent).encode()).hexdigest()[:12],
        'unique_fingerprint': hashlib.sha256((client_ip + user_agent + str(request.headers.get('Accept-Language', ''))).encode()).hexdigest()[:16],
        'cookies_enabled': 'Detected via JavaScript',
        'local_storage': 'Detected via JavaScript',
        'session_storage': 'Detected via JavaScript',
        'canvas_fingerprint': 'Detected via JavaScript',
        'webgl_fingerprint': 'Detected via JavaScript',
        'audio_fingerprint': 'Detected via JavaScript',
        'font_fingerprint': 'Detected via JavaScript',
        
        # Request Details
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
        'json_data': request.get_json() if request.is_json else None,
        
        # All HTTP Headers (for educational purposes)
        'all_headers': dict(request.headers),
        'header_count': len(request.headers),
        
        # Privacy Indicators
        'privacy_score': calculate_privacy_score(request),
        'tracking_risk': assess_tracking_risk(request),
    }
    
    return jsonify(exposure_data)

@app.route('/privacy-tips')
def privacy_tips():
    """Additional endpoint with privacy protection tips"""
    tips = {
        'immediate_actions': [
            'Use a VPN service to hide your IP address',
            'Install uBlock Origin or similar ad blocker',
            'Use Firefox with strict privacy settings',
            'Regularly clear cookies and browsing data',
            'Disable location services for browsers',
        ],
        'advanced_protection': [
            'Use Tor browser for sensitive activities',
            'Install Privacy Badger extension',
            'Use DuckDuckGo instead of Google',
            'Consider using Brave browser',
            'Use ProtonMail for private email',
        ],
        'organizational_tips': [
            'Implement privacy training for staff',
            'Use privacy-focused tools and services',
            'Regular security audits of web applications',
            'Educate about digital footprint risks',
        ]
    }
    return jsonify(tips)

def print_startup_info():
    """Print information for the facilitator"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("🕵️" * 30)
    print("   HTTP DATA EXPOSURE DEMONSTRATION")
    print("🕵️" * 30)
    print(f"\n🌐 Server running on:")
    print(f"   Local:    http://localhost:5000")
    print(f"   Network:  http://{local_ip}:5000")
    print(f"\n📋 FACILITATOR INSTRUCTIONS:")
    print(f"   1. Share the network URL with participants")
    print(f"   2. Have them visit the page on their devices")
    print(f"   3. Ask them to click 'REVEAL MY DATA EXPOSURE'")
    print(f"   4. Discuss what they see and privacy implications")
    print(f"   5. Use /privacy-tips endpoint for solutions")
    print(f"\n💡 DISCUSSION POINTS:")
    print(f"   • How much can websites learn about you?")
    print(f"   • Why is this data valuable to companies?")
    print(f"   • What can organizations do to protect privacy?")
    print(f"   • How can individuals protect themselves?")
    print(f"\n🎯 Learning Objective: Awareness of digital footprint")
    print("🕵️" * 30)

if __name__ == '__main__':
    print_startup_info()
    
    # Run the Flask application
    # Use 0.0.0.0 to allow network access from other devices
    app.run(host='0.0.0.0', port=5000, debug=True)