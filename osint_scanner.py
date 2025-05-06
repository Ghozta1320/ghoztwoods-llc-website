import requests
import re
import json
import phonenumbers
from phonenumbers import geocoder, carrier
from datetime import datetime
import socket
import whois
import os
from typing import Dict, Any, List

class OSINTScanner:
    def __init__(self):
        # Load threat intelligence data
        self.threat_db = self._load_threat_db()
        
        # Setup cache directory
        self.cache_dir = os.path.join("data", "osint_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _load_threat_db(self) -> Dict:
        """Load local threat intelligence database"""
        try:
            with open(os.path.join("data", "threat_intel.json"), 'r') as f:
                return json.load(f)
        except:
            return {
                "malicious_ips": [],
                "suspicious_domains": [],
                "known_breaches": {}
            }
            
    def scan_target(self, target_info: str) -> Dict[str, Any]:
        """Main scanning method that coordinates all OSINT operations"""
        results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": target_info,
            "findings": {},
            "analysis": {
                "risk_level": "low",
                "threats_found": 0,
                "data_sources": {
                    "online": [],
                    "offline": ["local_threat_db"]
                }
            }
        }
        
        # Extract and analyze emails
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', target_info)
        if emails:
            results["findings"]["emails"] = self._analyze_emails(emails)
            
        # Extract and analyze phone numbers
        phones = re.findall(r'\+?1?\d{9,15}', target_info)
        if phones:
            results["findings"]["phones"] = self._analyze_phones(phones)
            
        # Extract and analyze IPs
        ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', target_info)
        if ips:
            results["findings"]["ips"] = self._analyze_ips(ips)
            
        # Extract and analyze domains
        domains = re.findall(r'(?:https?:\/\/)?(?:[\w-]+\.)+[\w-]+', target_info)
        if domains:
            results["findings"]["domains"] = self._analyze_domains(domains)
            
        # Perform final analysis
        self._analyze_findings(results)
        
        return results
        
    def _analyze_emails(self, emails: List[str]) -> List[Dict]:
        """Analyze email addresses"""
        results = []
        for email in emails:
            analysis = {
                "email": email,
                "domain": email.split('@')[1],
                "threats": [],
                "breach_status": "unknown"
            }
            
            # Check domain against threat database
            if analysis["domain"] in self.threat_db["known_breaches"]:
                breach = self.threat_db["known_breaches"][analysis["domain"]]
                analysis["threats"].append({
                    "type": "data_breach",
                    "details": breach
                })
                analysis["breach_status"] = "confirmed"
                
            # Try online breach check
            try:
                response = requests.get(
                    f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                    headers={"User-Agent": "OSINT Research"}
                )
                if response.status_code == 200:
                    analysis["threats"].append({
                        "type": "online_breach",
                        "details": "Found in online breach database"
                    })
                    analysis["breach_status"] = "confirmed"
            except:
                pass
                
            results.append(analysis)
        return results
        
    def _analyze_phones(self, phones: List[str]) -> List[Dict]:
        """Analyze phone numbers"""
        results = []
        for phone in phones:
            try:
                parsed = phonenumbers.parse(phone)
                analysis = {
                    "number": phone,
                    "valid": phonenumbers.is_valid_number(parsed),
                    "location": {
                        "country": geocoder.description_for_number(parsed, "en"),
                        "carrier": carrier.name_for_number(parsed, "en")
                    },
                    "threats": []
                }
                results.append(analysis)
            except Exception as e:
                results.append({
                    "number": phone,
                    "error": str(e)
                })
        return results
        
    def _analyze_ips(self, ips: List[str]) -> List[Dict]:
        """Analyze IP addresses"""
        results = []
        for ip in ips:
            analysis = {
                "ip": ip,
                "threats": []
            }
            
            # Check against known malicious IPs
            if ip in self.threat_db["malicious_ips"]:
                analysis["threats"].append({
                    "type": "known_malicious",
                    "source": "local_threat_db"
                })
                
            # Try to get geolocation
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}")
                if response.status_code == 200:
                    analysis["geolocation"] = response.json()
            except:
                analysis["geolocation"] = "Failed to retrieve"
                
            results.append(analysis)
        return results
        
    def _analyze_domains(self, domains: List[str]) -> List[Dict]:
        """Analyze domain names"""
        results = []
        for domain in domains:
            domain = domain.replace("http://", "").replace("https://", "").split('/')[0]
            analysis = {
                "domain": domain,
                "threats": []
            }
            
            # Check against suspicious domains
            if domain in self.threat_db["suspicious_domains"]:
                analysis["threats"].append({
                    "type": "suspicious_domain",
                    "source": "local_threat_db"
                })
                
            # Try to get WHOIS info
            try:
                w = whois.whois(domain)
                analysis["whois"] = {
                    "registrar": w.registrar,
                    "creation_date": str(w.creation_date),
                    "expiration_date": str(w.expiration_date)
                }
            except:
                analysis["whois"] = "Failed to retrieve"
                
            results.append(analysis)
        return results
        
    def _analyze_findings(self, results: Dict):
        """Perform final analysis of all findings"""
        threat_count = 0
        risk_score = 0
        
        # Analyze email threats
        if "emails" in results["findings"]:
            for email in results["findings"]["emails"]:
                threat_count += len(email.get("threats", []))
                if email.get("breach_status") == "confirmed":
                    risk_score += 20
                    
        # Analyze IP threats
        if "ips" in results["findings"]:
            for ip in results["findings"]["ips"]:
                threats = ip.get("threats", [])
                threat_count += len(threats)
                if any(t["type"] == "known_malicious" for t in threats):
                    risk_score += 30
                    
        # Analyze domain threats
        if "domains" in results["findings"]:
            for domain in results["findings"]["domains"]:
                threats = domain.get("threats", [])
                threat_count += len(threats)
                if any(t["type"] == "suspicious_domain" for t in threats):
                    risk_score += 25
                    
        # Update analysis
        results["analysis"].update({
            "risk_level": "critical" if risk_score > 60 else "high" if risk_score > 40 else "medium" if risk_score > 20 else "low",
            "risk_score": risk_score,
            "threats_found": threat_count,
            "recommendations": self._generate_recommendations(risk_score, threat_count)
        })
        
    def _generate_recommendations(self, risk_score: int, threat_count: int) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if risk_score > 60:
            recommendations.extend([
                "URGENT: Immediate security audit recommended",
                "Enable enhanced monitoring on all accounts",
                "Change all associated passwords",
                "Enable two-factor authentication where possible"
            ])
        elif risk_score > 40:
            recommendations.extend([
                "Review and update security measures",
                "Monitor for suspicious activities",
                "Consider enabling additional security features"
            ])
        elif risk_score > 20:
            recommendations.extend([
                "Regular security review recommended",
                "Keep monitoring for changes"
            ])
        else:
            recommendations.append("Maintain current security measures")
            
        return recommendations

if __name__ == "__main__":
    scanner = OSINTScanner()
    print("OSINT Scanner initialized with threat intelligence database")
    print("Ready for scanning...")
