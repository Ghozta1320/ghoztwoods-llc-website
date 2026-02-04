"""
GHOZTWOODS LLC - Scam Intelligence API
Backend proxy for Hugging Face AI to avoid CORS and protect API keys
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for GitHub Pages

# Hugging Face Configuration
HF_API_URL = 'https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2'
HF_API_KEY = os.getenv('HF_API_KEY')
if not HF_API_KEY:
    raise ValueError("HF_API_KEY environment variable not set")

# System prompt for IC-level analysis
SYSTEM_PROMPT = """You are an elite intelligence analyst for GHOZTWOODS LLC, specializing in scam investigation using Intelligence Community (IC) methodologies:

- GEOINT (Geospatial Intelligence): Analyze location data, IP addresses, geographic patterns
- SOCINT (Social Media Intelligence): Investigate social media profiles, connections, behavior patterns  
- HUMINT (Human Intelligence): Analyze human behavior, psychology, social engineering tactics
- OSINT (Open Source Intelligence): Research public records, databases, online footprints
- SIGINT (Signals Intelligence): Analyze communication patterns, metadata, digital signatures

When analyzing scams, provide:
1. Detailed threat assessment with risk level
2. Geographic analysis if location data available
3. Social engineering tactics used
4. Recommended countermeasures
5. Evidence collection guidance
6. Reporting procedures

Be thorough, technical, and provide actionable intelligence. Use IC terminology and methodologies."""

@app.route('/api/analyze', methods=['POST'])
def analyze_threat():
    """Analyze threat using Hugging Face AI"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Build prompt
        prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\n\nAssistant:"
        
        # Call Hugging Face API
        response = requests.post(
            HF_API_URL,
            headers={
                'Authorization': f'Bearer {HF_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'inputs': prompt,
                'parameters': {
                    'max_new_tokens': 500,
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'return_full_text': False
                }
            },
            timeout=30
        )
        
        if response.status_code != 200:
            return jsonify({
                'error': f'Hugging Face API error: {response.status_code}',
                'details': response.text
            }), 500
        
        result = response.json()
        ai_response = result[0].get('generated_text', 'Unable to generate response')
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'GHOZTWOODS Scam Intelligence API',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
