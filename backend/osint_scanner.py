import requests
import json
from rich.console import Console
from rich import print as rprint
import time
import re
from typing import Dict, Any, List
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import whois
import dns.resolver
import socket
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime

class OSINTScanner:
    def __init__(self):
        self.console = Console()
        self.api_keys = self._load_api_keys()

    def _load_api_keys(self) -> Dict[str, str]:
        try:
            with open('config/api_keys.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def analyze_phone(self, phone: str) -> Dict[str, Any]:
        results = {
            "carrier_info": {},
            "location_data": {},
            "reputation": {},
            "social_media": [],
            "data_breaches": [],
            "risk_factors": []
        }

        try:
            # Parse phone number
            parsed = phonenumbers.parse(phone)
            
            # Carrier Information
            results["carrier_info"] = {
                "carrier": carrier.name_for_number(parsed, "en"),
                "valid": phonenumbers.is_valid_number(parsed),
                "type": phonenumbers.number_type(parsed),
                "region": geocoder.description_for_number(parsed, "en"),
                "timezones": timezone.time_zones_for_number(parsed)
            }

            # Sync.me Integration
            syncme_data = self._query_syncme(phone)
            if syncme_data:
                results["social_media"].extend(syncme_data)

            # PhoneInfoga Analysis
            infoga_data = self._analyze_with_phoneinfoga(phone)
            results["location_data"].update(infoga_data.get("location", {}))
            results["reputation"].update(infoga_data.get("reputation", {}))

            # WhitePages & Spokeo
            whitepages_data = self._query_whitepages(phone)
            spokeo_data = self._query_spokeo(phone)
            
            results["data_breaches"] = self._check_breaches(phone)
            
            # Risk Assessment
            risk_factors = []
            if results["reputation"].get("spam_score", 0) > 0.7:
                risk_factors.append("High spam score detected")
            if results["data_breaches"]:
                risk_factors.append(f"Found in {len(results['data_breaches'])} data breaches")
            if results["carrier_info"].get("type") == "VOIP":
                risk_factors.append("VOIP number - commonly used in scams")
                
            results["risk_factors"] = risk_factors
            results["risk_score"] = self._calculate_risk_score(results)

        except Exception as e:
            results["error"] = str(e)

        return results

    def analyze_email(self, email: str) -> Dict[str, Any]:
        results = {
            "validation": {},
            "breaches": [],
            "social_profiles": [],
            "domain_info": {},
            "risk_factors": []
        }

        try:
            # Email Format Validation
            results["validation"] = self._validate_email_format(email)

            # DeHashed Database Check
            dehashed_data = self._query_dehashed(email)
            if dehashed_data:
                results["breaches"].extend(dehashed_data)

            # Intelligence X Integration
            intell_x_data = self._query_intelligence_x(email)
            results["domain_info"].update(intell_x_data.get("domain_info", {}))

            # Holehe Social Media Check
            social_data = self._check_social_media(email)
            results["social_profiles"].extend(social_data)

            # Snov.io Pattern Analysis
            pattern_data = self._analyze_email_pattern(email)
            results["pattern_analysis"] = pattern_data

            # Risk Assessment
            risk_factors = []
            if len(results["breaches"]) > 0:
                risk_factors.append(f"Found in {len(results['breaches'])} data breaches")
            if results["validation"].get("disposable", False):
                risk_factors.append("Disposable email detected")
            if len(results["social_profiles"]) == 0:
                risk_factors.append("No legitimate social media presence found")

            results["risk_factors"] = risk_factors
            results["risk_score"] = self._calculate_risk_score(results)

        except Exception as e:
            results["error"] = str(e)

        return results

    def analyze_domain(self, domain: str) -> Dict[str, Any]:
        results = {
            "whois_data": {},
            "dns_records": {},
            "security_info": {},
            "historical_data": [],
            "connected_domains": [],
            "risk_factors": []
        }

        try:
            # SecurityTrails Historical Data
            historical_data = self._query_securitytrails(domain)
            results["historical_data"] = historical_data

            # Censys Infrastructure Analysis
            infrastructure = self._analyze_infrastructure(domain)
            results["security_info"].update(infrastructure)

            # DNS Investigation
            dns_data = self._analyze_dns(domain)
            results["dns_records"] = dns_data

            # SpyOnWeb Connected Domains
            connected = self._find_connected_domains(domain)
            results["connected_domains"] = connected

            # ThreatCrowd Intelligence
            threat_data = self._query_threatcrowd(domain)
            results["threat_intel"] = threat_data

            # Wayback Machine History
            wayback_data = self._query_wayback(domain)
            results["historical_snapshots"] = wayback_data

            # Risk Assessment
            risk_factors = []
            if results["security_info"].get("ssl_issues"):
                risk_factors.append("SSL certificate issues detected")
            if results["threat_intel"].get("malicious_score", 0) > 0.5:
                risk_factors.append("High malicious activity score")
            if len(results["connected_domains"]) > 50:
                risk_factors.append("Unusually high number of connected domains")

            results["risk_factors"] = risk_factors
            results["risk_score"] = self._calculate_risk_score(results)

        except Exception as e:
            results["error"] = str(e)

        return results

    def analyze_crypto(self, address: str) -> Dict[str, Any]:
        results = {
            "transaction_history": {},
            "wallet_analysis": {},
            "cluster_info": {},
            "risk_assessment": {},
            "risk_factors": []
        }

        try:
            # Blockchair Analytics
            blockchair_data = self._query_blockchair(address)
            results["transaction_history"] = blockchair_data

            # WalletExplorer Clustering
            cluster_data = self._analyze_wallet_cluster(address)
            results["cluster_info"] = cluster_data

            # BitcoinWhosWho Intelligence
            whowho_data = self._query_bitcoinwhoswho(address)
            results["wallet_analysis"].update(whowho_data)

            # Ethplorer & Bloxy Analysis (for Ethereum addresses)
            if self._is_eth_address(address):
                eth_data = self._analyze_eth_address(address)
                results["wallet_analysis"].update(eth_data)

            # Breadcrumbs Visualization
            breadcrumbs_data = self._generate_transaction_map(address)
            results["transaction_map"] = breadcrumbs_data

            # TokenView Transaction Tracking
            token_data = self._track_token_transactions(address)
            results["token_transactions"] = token_data

            # Risk Assessment
            risk_factors = []
            if results["wallet_analysis"].get("mixing_service_usage"):
                risk_factors.append("Connected to mixing services")
            if results["cluster_info"].get("dark_market_association"):
                risk_factors.append("Associated with dark markets")
            if results["transaction_history"].get("high_risk_patterns"):
                risk_factors.append("Suspicious transaction patterns detected")

            results["risk_factors"] = risk_factors
            results["risk_score"] = self._calculate_risk_score(results)

        except Exception as e:
            results["error"] = str(e)

        return results

    def _calculate_risk_score(self, data: Dict[str, Any]) -> float:
        """Calculate a risk score based on analysis results"""
        score = 0.0
        weight = 1.0
        
        if "risk_factors" in data:
            score += len(data["risk_factors"]) * 0.1

        if "breaches" in data:
            score += len(data.get("breaches", [])) * 0.05

        if "reputation" in data:
            spam_score = data["reputation"].get("spam_score", 0)
            score += spam_score * 0.3

        return min(1.0, score * weight)

    def _query_syncme(self, phone: str) -> List[Dict[str, Any]]:
        """Query Sync.me API for social media profiles"""
        # Implementation for Sync.me API integration
        return []

    def _analyze_with_phoneinfoga(self, phone: str) -> Dict[str, Any]:
        """Analyze phone number using PhoneInfoga"""
        # Implementation for PhoneInfoga integration
        return {"location": {}, "reputation": {}}

    def _query_whitepages(self, phone: str) -> Dict[str, Any]:
        """Query WhitePages for phone information"""
        # Implementation for WhitePages API integration
        return {}

    def _query_spokeo(self, phone: str) -> Dict[str, Any]:
        """Query Spokeo for phone information"""
        # Implementation for Spokeo API integration
        return {}

    def _check_breaches(self, identifier: str) -> List[Dict[str, Any]]:
        """Check for data breaches containing the identifier"""
        # Implementation for breach checking
        return []

    def _validate_email_format(self, email: str) -> Dict[str, bool]:
        """Validate email format and check for disposable email services"""
        # Implementation for email validation
        return {"valid": bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))}

    def _query_dehashed(self, email: str) -> List[Dict[str, Any]]:
        """Query DeHashed database for breached data"""
        # Implementation for DeHashed API integration
        return []

    def _query_intelligence_x(self, email: str) -> Dict[str, Any]:
        """Query Intelligence X for email information"""
        # Implementation for Intelligence X API integration
        return {"domain_info": {}}

    def _check_social_media(self, email: str) -> List[Dict[str, Any]]:
        """Check social media presence using Holehe"""
        # Implementation for Holehe integration
        return []

    def _analyze_email_pattern(self, email: str) -> Dict[str, Any]:
        """Analyze email pattern using Snov.io"""
        # Implementation for Snov.io API integration
        return {}

    def _query_securitytrails(self, domain: str) -> List[Dict[str, Any]]:
        """Query SecurityTrails for domain history"""
        return []

    def _analyze_infrastructure(self, domain: str) -> Dict[str, Any]:
        """Analyze domain infrastructure using Censys"""
        return {}

    def _analyze_dns(self, domain: str) -> Dict[str, Any]:
        """Analyze DNS records"""
        return {}

    def _find_connected_domains(self, domain: str) -> List[str]:
        """Find connected domains using SpyOnWeb"""
        return []

    def _query_threatcrowd(self, domain: str) -> Dict[str, Any]:
        """Query ThreatCrowd for domain intelligence"""
        return {}

    def _query_wayback(self, domain: str) -> List[Dict[str, Any]]:
        """Query Wayback Machine for domain history"""
        return []

    def _query_blockchair(self, address: str) -> Dict[str, Any]:
        """Query Blockchair for crypto transaction history"""
        return {}

    def _analyze_wallet_cluster(self, address: str) -> Dict[str, Any]:
        """Analyze wallet clusters using WalletExplorer"""
        return {}

    def _query_bitcoinwhoswho(self, address: str) -> Dict[str, Any]:
        """Query BitcoinWhosWho for wallet intelligence"""
        return {}

    def _analyze_eth_address(self, address: str) -> Dict[str, Any]:
        """Analyze Ethereum address using Ethplorer/Bloxy"""
        return {}

    def _generate_transaction_map(self, address: str) -> Dict[str, Any]:
        """Generate transaction map using Breadcrumbs"""
        return {}

    def _track_token_transactions(self, address: str) -> Dict[str, Any]:
        """Track token transactions using TokenView"""
        return {}

    def _is_eth_address(self, address: str) -> bool:
        """Check if address is a valid Ethereum address"""
        return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))
