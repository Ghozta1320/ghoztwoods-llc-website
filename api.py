from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from osint_scanner import OSINTScanner
from audio_processing import AudioAnalyzer
from geo_tracker import GeoTracker
from datetime import datetime
import json
import os
from typing import Dict, Any

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize scanner
scanner = OSINTScanner()

def save_scan_result(scan_type: str, target: str, result: Dict[str, Any]):
    """Save scan results to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"findings/{scan_type}_scans/scan_{timestamp}.json"
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    data = {
        "timestamp": timestamp,
        "target": target,
        "type": scan_type,
        "result": result
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/api/audio-analysis', methods=['POST'])
def analyze_audio():
    """Handle audio analysis requests"""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
        
    try:
        audio_file = request.files['audio']
        analyzer = AudioAnalyzer()
        results = analyzer.analyze_audio(audio_file)
        
        return jsonify({
            "status": "success",
            "result": results
        })
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in scan endpoint: {error_trace}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": error_trace
        }), 500

@app.route('/api/sigint', methods=['POST'])
def analyze_signals():
    """Handle SIGINT analysis requests"""
    data = request.json
    target = data.get('target')
    
    if not target:
        return jsonify({"error": "No target provided"}), 400
        
    try:
        # Initialize signal analysis
        results = {
            "signal_strength": [],
            "frequency_analysis": {},
            "transmission_patterns": [],
            "anomalies": []
        }
        
        # Add signal analysis logic here
        # This is a placeholder for actual SIGINT capabilities
        
        return jsonify({
            "status": "success",
            "result": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/geo-track', methods=['POST'])
def track_location():
    """Handle geolocation tracking requests"""
    data = request.json
    target = data.get('target')
    
    if not target:
        return jsonify({"error": "No target provided"}), 400
        
    try:
        tracker = GeoTracker()
        results = tracker.track_location(target)
        
        return jsonify({
            "status": "success",
            "result": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.json
    target = data.get('target')
    scan_type = data.get('type', 'all')

    print(f"Scan request received. Target: {target}, Type: {scan_type}")

    if not target:
        return jsonify({"error": "No target provided"}), 400

    try:
        results = {}
        
        # Determine target type and run appropriate scans
        if '@' in target:  # Email analysis
            results['email'] = scanner.analyze_email(target)
            
        elif target.startswith(('0x', '1', '3', 'bc')):  # Crypto address
            results['crypto'] = scanner.analyze_crypto(target)
            
        elif any(c.isdigit() for c in target):  # Phone number
            results['phone'] = scanner.analyze_phone(target)
            
        else:  # Domain/URL analysis
            results['domain'] = scanner.analyze_domain(target)

        # Save results
        save_scan_result(scan_type, target, results)

        return jsonify({
            "status": "success",
            "result": results
        })

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in scan endpoint: {error_trace}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "trace": error_trace
        }), 500

@app.route('/api/submit-tip', methods=['POST'])
def submit_tip():
    """Handle tip submissions"""
    data = request.json
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"findings/tips/tip_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        # TODO: Add notification system for urgent tips
        if data.get('urgency') == 'high':
            # Implement notification system
            pass
        
        return jsonify({
            "status": "success",
            "message": "Tip submitted successfully"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/phone-intel', methods=['POST'])
def phone_intel():
    """Enhanced phone number intelligence endpoint"""
    data = request.json
    phone = data.get('target')
    
    if not phone:
        return jsonify({"error": "No phone number provided"}), 400
        
    try:
        results = scanner.analyze_phone(phone)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/email-analysis', methods=['POST'])
def email_analysis():
    """Enhanced email analysis endpoint"""
    data = request.json
    email = data.get('target')
    
    if not email:
        return jsonify({"error": "No email provided"}), 400
        
    try:
        results = scanner.analyze_email(email)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/domain-recon', methods=['POST'])
def domain_recon():
    """Enhanced domain reconnaissance endpoint"""
    data = request.json
    domain = data.get('target')
    
    if not domain:
        return jsonify({"error": "No domain provided"}), 400
        
    try:
        results = scanner.analyze_domain(domain)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crypto-investigation', methods=['POST'])
def crypto_investigation():
    """Enhanced cryptocurrency investigation endpoint"""
    data = request.json
    address = data.get('target')
    
    if not address:
        return jsonify({"error": "No crypto address provided"}), 400
        
    try:
        results = scanner.analyze_crypto(address)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health_check():
    """API health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
