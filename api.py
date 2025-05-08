from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from datetime import datetime
import json
import os
import requests
import socket
import whois
import dns.resolver
import phonenumbers
from phonenumbers import geocoder, carrier
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

# API Keys for various OSINT services
API_KEYS = {
    "whois": "sk_f2f9df69d34d124f1b542a2d45964100",  # Whoisxmlapi.com
    "hibp": "3fdb6956-5e8c-4591-8d7f-1561e5341524",  # HaveIBeenPwned
    "hunter": "7ce7ec5d5fba4f3d8f7d7eb31244f0c2d8f99b5a",  # Hunter.io
    "fullcontact": "sk_f2f9df69d34d124f1b542a2d45964100",  # FullContact
    "virustotal": "e2513a75f8133a4876045afe355deda6c4d80c3b7c54951d54198b5d12057fd8",  # VirusTotal
    "shodan": "PSKINdQe1GyxGgecYz2191H2JoS9qvgD"  # Shodan
}

def perform_phone_intel(phone):
    """Comprehensive phone number intelligence gathering"""
    try:
        parsed = phonenumbers.parse(phone)
        results = {
            "carrier": carrier.name_for_number(parsed, "en"),
            "location": geocoder.description_for_number(parsed, "en"),
            "valid": phonenumbers.is_valid_number(parsed),
            "type": "MOBILE" if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE else "LANDLINE"
        }

        # Additional OSINT gathering
        try:
            # Check phone reputation databases
            truecaller_url = f"https://search5-noneu.truecaller.com/v2/search"
            headers = {
                "Authorization": f"Bearer {API_KEYS['truecaller']}",
                "Content-Type": "application/json"
            }
            response = requests.get(truecaller_url, headers=headers)
            if response.status_code == 200:
                results["reputation"] = response.json()
        except:
            results["reputation"] = "Lookup failed"

        # Search for phone number mentions
        try:
            # Google dorks for phone number
            search_query = f"{phone} scam OR fraud OR spam site:reddit.com OR site:scam.com"
            results["web_mentions"] = perform_google_search(search_query)
        except:
            results["web_mentions"] = []

        return results
    except Exception as e:
        return {"error": str(e)}

def perform_email_analysis(email):
    """Comprehensive email intelligence gathering"""
    try:
        results = {
            "domain": email.split('@')[1],
            "username": email.split('@')[0],
            "valid_format": bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
        }

        # Check HaveIBeenPwned
        try:
            headers = {
                "hibp-api-key": API_KEYS["hibp"],
                "user-agent": "OSINT-Scanner"
            }
            response = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                headers=headers
            )
            if response.status_code == 200:
                results["breaches"] = response.json()
            else:
                results["breaches"] = []
        except:
            results["breaches"] = "Lookup failed"

        # Check Hunter.io for email verification
        try:
            hunter_url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={API_KEYS['hunter']}"
            response = requests.get(hunter_url)
            if response.status_code == 200:
                results["verification"] = response.json()
        except:
            results["verification"] = "Verification failed"

        # Search for social profiles
        try:
            fullcontact_url = "https://api.fullcontact.com/v3/person.enrich"
            headers = {
                "Authorization": f"Bearer {API_KEYS['fullcontact']}",
                "Content-Type": "application/json"
            }
            data = {"email": email}
            response = requests.post(fullcontact_url, headers=headers, json=data)
            if response.status_code == 200:
                results["social_profiles"] = response.json()
        except:
            results["social_profiles"] = "Lookup failed"

        return results
    except Exception as e:
        return {"error": str(e)}

def perform_domain_recon(domain):
    """Comprehensive domain reconnaissance"""
    try:
        results = {
            "whois": get_whois_info(domain),
            "dns_records": get_dns_records(domain),
            "ssl_info": get_ssl_info(domain),
            "headers": get_http_headers(domain)
        }

        # Check VirusTotal
        try:
            vt_url = f"https://www.virustotal.com/vtapi/v2/domain/report"
            params = {"apikey": API_KEYS["virustotal"], "domain": domain}
            response = requests.get(vt_url, params=params)
            if response.status_code == 200:
                results["security_info"] = response.json()
        except:
            results["security_info"] = "Lookup failed"

        # Check Shodan
        try:
            shodan_url = f"https://api.shodan.io/shodan/host/search?key={API_KEYS['shodan']}&query=hostname:{domain}"
            response = requests.get(shodan_url)
            if response.status_code == 200:
                results["infrastructure"] = response.json()
        except:
            results["infrastructure"] = "Lookup failed"

        return results
    except Exception as e:
        return {"error": str(e)}

def get_whois_info(domain):
    """Get WHOIS information for domain"""
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers
        }
    except:
        return "WHOIS lookup failed"

def get_dns_records(domain):
    """Get DNS records for domain"""
    records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(answer) for answer in answers]
        except:
            records[record_type] = []
    return records

def get_ssl_info(domain):
    """Get SSL certificate information"""
    try:
        response = requests.get(f"https://{domain}", verify=False)
        return {
            "issuer": response.raw.connection.cert.get_issuer().get_components(),
            "subject": response.raw.connection.cert.get_subject().get_components(),
            "version": response.raw.connection.cert.get_version(),
            "expired": response.raw.connection.cert.has_expired()
        }
    except:
        return "SSL lookup failed"

def get_http_headers(domain):
    """Get HTTP headers from domain"""
    try:
        response = requests.head(f"https://{domain}")
        return dict(response.headers)
    except:
        return "Header lookup failed"

def perform_google_search(query):
    """Perform Google search with custom query"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(
            f"https://www.google.com/search?q={query}",
            headers=headers
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text if g.find('h3') else 'No title'
                snippet = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else 'No snippet'
                results.append({
                    "title": title,
                    "link": link,
                    "snippet": snippet
                })
        return results
    except Exception as e:
        return []

@app.route('/api/scan', methods=['POST'])
async def scan():
    data = request.json
    if not data or 'target' not in data:
        return jsonify({"error": "No target provided"}), 400

    target = data['target']
    results = {
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "scan_type": data.get('type', 'full'),
        "results": {}
    }

    # Determine target type and perform appropriate scans
    if re.match(r"^\+?[\d\s-]+$", target):  # Phone number
        results["results"]["phone"] = perform_phone_intel(target)
    elif re.match(r"[^@]+@[^@]+\.[^@]+", target):  # Email
        results["results"]["email"] = perform_email_analysis(target)
    elif re.match(r"^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,}$", target):  # Domain
        results["results"]["domain"] = perform_domain_recon(target)
    elif re.match(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$", target):  # Crypto address
        results["results"]["crypto"] = perform_crypto_investigation(target)

    return jsonify(results)

@app.route('/api/phone-intel', methods=['POST'])
async def phone_intel():
    data = request.json
    if not data or 'target' not in data:
        return jsonify({"error": "No target provided"}), 400
    
    results = perform_phone_intel(data['target'])
    return jsonify(results)

@app.route('/api/email-analysis', methods=['POST'])
async def email_analysis():
    data = request.json
    if not data or 'target' not in data:
        return jsonify({"error": "No target provided"}), 400
    
    results = perform_email_analysis(data['target'])
    return jsonify(results)

@app.route('/api/domain-recon', methods=['POST'])
async def domain_recon():
    data = request.json
    if not data or 'target' not in data:
        return jsonify({"error": "No target provided"}), 400
    
    results = perform_domain_recon(data['target'])
    return jsonify(results)

@app.route('/api/health')
def health_check():
    """API health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
