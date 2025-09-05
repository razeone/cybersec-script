#!/usr/bin/env python3
"""
🕵️ HTTP REQUEST DATA EXPOSURE DEMONSTRATION (Enhanced)
Shows participants exactly what data they reveal with every web request
Perfect for cybersecurity awareness training!
Now with enhanced cookie, header, and fingerprinting data collection
"""

from flask import Flask, request, jsonify, render_template_string, make_response
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
    <title>🔍 Enhanced Data Exposure Demo - See What You Really Share!</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 900px; 
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
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            max-height: 500px;
            overflow-y: auto;
            display: none;
        }
        .privacy-score {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-weight: bold;
            text-align: center;
        }
        .score-high { background: #4CAF50; }
        .score-medium { background: #FF9800; }
        .score-low { background: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Enhanced Privacy Exposure Demo</h1>
        
        <div class="warning">
            ⚠️ WARNING: This demonstration will reveal EXTENSIVE information about your device and browsing habits!
        </div>
        
        <div class="demo-controls">
            <h3>Demo Controls:</h3>
            <button class="demo-btn" onclick="setCookies()">🍪 Set Demo Cookies</button>
            <button class="demo-btn danger" onclick="clearCookies()">🗑️ Clear Cookies</button>
            <button class="demo-btn" onclick="showFingerprint()">👆 Browser Fingerprint</button>
        </div>
        
        <p style="text-align: center; font-size: 1.2em;">
            Click the button below to see exactly what information websites can collect about you:
        </p>
        
        <button class="reveal-btn" onclick="revealDataExposure()">
            🕵️ REVEAL MY ENHANCED DATA EXPOSURE 🕵️
        </button>
        
        <div id="results"></div>
        
        <div style="margin-top: 30px; text-align: center; font-size: 0.9em; opacity: 0.8;">
            <p>🎯 Educational Purpose: Understanding Digital Privacy</p>
            <p>Visit <a href="/privacy-tips" style="color: #FFD700;">Privacy Tips</a> for protection strategies</p>
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
                    document.getElementById('results').innerHTML = JSON.stringify(data, null, 2);
                });
        }
        
        // Main data exposure function
        function revealDataExposure() {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = 'Collecting your data... 🕵️';
            
            // Include client-side data
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
                // Format the results nicely
                let output = "🔍 YOUR DATA EXPOSURE ANALYSIS\\n";
                output += "=".repeat(50) + "\\n\\n";
                
                // Privacy Score
                const score = data.privacy_score || 50;
                let scoreClass = score > 70 ? 'score-high' : score > 40 ? 'score-medium' : 'score-low';
                let scoreText = score > 70 ? 'GOOD' : score > 40 ? 'FAIR' : 'POOR';
                
                output += `🛡️ PRIVACY SCORE: ${score}/100 (${scoreText})\\n`;
                output += `🚨 TRACKING RISK: ${data.tracking_risk?.level || 'UNKNOWN'}\\n\\n`;
                
                // Network Information
                output += "🌐 NETWORK & LOCATION:\\n";
                output += `   IP Address: ${data.ip_address}\\n`;
                output += `   Location: ${data.location}\\n`;
                output += `   ISP: ${data.isp}\\n`;
                output += `   Connection: ${data.connection_type}\\n\\n`;
                
                // Device Information
                output += "💻 DEVICE & BROWSER:\\n";
                output += `   OS: ${data.os_info}\\n`;
                output += `   Browser: ${data.browser}\\n`;
                output += `   Language: ${data.language}\\n`;
                output += `   Do Not Track: ${data.do_not_track}\\n\\n`;
                
                // Cookies & Tracking
                output += "🍪 COOKIES & TRACKING:\\n";
                output += `   Cookie Count: ${data.cookie_count}\\n`;
                output += `   Has Session Cookies: ${data.has_session_cookies}\\n`;
                output += `   Has Tracking Cookies: ${data.has_tracking_cookies}\\n`;
                if (data.cookies && Object.keys(data.cookies).length > 0) {
                    output += "   Active Cookies:\\n";
                    Object.keys(data.cookies).forEach(cookie => {
                        output += `     - ${cookie}: ${data.cookies[cookie]}\\n`;
                    });
                }
                output += "\\n";
                
                // Fingerprinting Data
                output += "👆 BROWSER FINGERPRINTING:\\n";
                output += `   Session ID: ${data.session_id}\\n`;
                output += `   Unique Fingerprint: ${data.unique_fingerprint}\\n`;
                if (window.clientInfo) {
                    output += `   Screen: ${window.clientInfo.screen_width}x${window.clientInfo.screen_height}\\n`;
                    output += `   Timezone: ${window.clientInfo.timezone}\\n`;
                    output += `   Canvas Fingerprint: ${window.clientInfo.canvas_fingerprint}\\n`;
                }
                output += "\\n";
                
                // Security Headers
                output += "🔒 SECURITY HEADERS:\\n";
                output += `   Sec-Fetch-Site: ${data.sec_fetch_site}\\n`;
                output += `   Sec-Fetch-Mode: ${data.sec_fetch_mode}\\n`;
                output += `   Origin: ${data.origin}\\n`;
                output += `   Referer: ${data.referer}\\n\\n`;
                
                // Risk Assessment
                if (data.tracking_risk && data.tracking_risk.factors) {
                    output += "⚠️ PRIVACY RISKS DETECTED:\\n";
                    data.tracking_risk.factors.forEach(factor => {
                        output += `   • ${factor}\\n`;
                    });
                    output += "\\n";
                }
                
                // Full data dump
                output += "📊 COMPLETE DATA DUMP:\\n";
                output += JSON.stringify(data, null, 2);
                
                resultsDiv.innerHTML = output;
            })
            .catch(error => {
                resultsDiv.innerHTML = 'Error collecting data: ' + error;
            });
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
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillText('Privacy Demo 🔍', 2, 2);
            return canvas.toDataURL().slice(-20);
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

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_request():
    """Analyze the request and return comprehensive data exposure information"""
    # Get client IP (handle proxies/load balancers)
    client_ip = request.headers.get('X-Forwarded-For', 
                request.headers.get('X-Real-IP', 
                request.remote_addr)).split(',')[0].strip()
    
    # Get location data
    location_data = get_ip_location(client_ip)
    
    # Parse user agent
    user_agent = request.headers.get('User-Agent', 'Unknown')
    os_info, browser_info = parse_user_agent(user_agent)
    
    # Collect comprehensive data
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
        'language': request.headers.get('Accept-Language', 'Unknown').split(',')[0],
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
        
        # Privacy Assessment
        'privacy_score': calculate_privacy_score(request),
        'tracking_risk': assess_tracking_risk(request),
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
    """Additional endpoint with privacy protection tips"""
    tips = {
        'immediate_actions': [
            'Use a VPN service to hide your IP address',
            'Install uBlock Origin or similar ad blocker',
            'Use Firefox with strict privacy settings',
            'Regularly clear cookies and browsing data',
            'Disable location services for browsers',
        ],
        'browser_settings': [
            'Enable "Do Not Track" in browser settings',
            'Disable third-party cookies',
            'Use private/incognito browsing mode',
            'Install privacy-focused browser extensions',
            'Consider using Tor Browser for sensitive activities'
        ],
        'advanced_protection': [
            'Use a privacy-focused DNS service (1.1.1.1, 9.9.9.9)',
            'Enable HTTPS Everywhere',
            'Use different browsers for different activities',
            'Consider using virtual machines for isolation',
            'Review and adjust social media privacy settings'
        ]
    }
    
    return jsonify(tips)

def print_startup_info():
    """Print startup information for facilitators"""
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = '127.0.1.1'
    
    print("🕵️" * 30)
    print("   ENHANCED HTTP DATA EXPOSURE DEMONSTRATION")
    print("🕵️" * 30)
    print(f"\n🌐 Server running on:")
    print(f"   Local:    http://localhost:5000")
    print(f"   Network:  http://{local_ip}:5000")
    print(f"\n📋 FACILITATOR INSTRUCTIONS:")
    print(f"   1. Share the network URL with participants")
    print(f"   2. Have them visit the page on their devices")
    print(f"   3. Ask them to click 'REVEAL MY ENHANCED DATA EXPOSURE'")
    print(f"   4. Try the cookie demo and fingerprint test")
    print(f"   5. Discuss what they see and privacy implications")
    print(f"   6. Use /privacy-tips endpoint for solutions")
    print(f"\n🆕 NEW FEATURES:")
    print(f"   • Enhanced cookie tracking demonstration")
    print(f"   • Browser fingerprinting analysis")
    print(f"   • Privacy score calculation")
    print(f"   • Security header analysis")
    print(f"   • Storage capability detection")
    print(f"\n💡 DISCUSSION POINTS:")
    print(f"   • How much can websites learn about you?")
    print(f"   • Why is this data valuable to companies?")
    print(f"   • What can organizations do to protect privacy?")
    print(f"   • How can individuals protect themselves?")
    print(f"\n🎯 Learning Objective: Comprehensive privacy awareness")
    print("🕵️" * 30)

if __name__ == '__main__':
    print_startup_info()
    
    # Run the Flask application
    # Use 0.0.0.0 to allow network access from other devices
    app.run(host='0.0.0.0', port=5000, debug=True)
