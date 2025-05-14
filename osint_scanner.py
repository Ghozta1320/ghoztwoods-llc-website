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
        try:
            api_key = self.api_keys.get("syncme")
            if not api_key:
                return []

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"https://api.sync.me/v1/phone/{phone}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                profiles = []
                
                if "social_profiles" in data:
                    for profile in data["social_profiles"]:
                        profiles.append({
                            "platform": profile.get("platform"),
                            "username": profile.get("username"),
                            "profile_url": profile.get("url"),
                            "last_seen": profile.get("last_seen"),
                            "followers": profile.get("followers_count"),
                            "verified": profile.get("verified", False)
                        })
                return profiles
        except Exception as e:
            self.console.print(f"[red]Error querying Sync.me: {str(e)}[/red]")
        return []

    def _analyze_with_phoneinfoga(self, phone: str) -> Dict[str, Any]:
        """Analyze phone number using PhoneInfoga and NumVerify"""
        try:
            numverify_key = self.api_keys.get("numverify")
            if not numverify_key:
                return {"location": {}, "reputation": {}}

            # NumVerify API for detailed carrier and location data
            response = requests.get(
                f"http://apilayer.net/api/validate",
                params={
                    "access_key": numverify_key,
                    "number": phone,
                    "format": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "location": {
                        "country": data.get("country_name"),
                        "region": data.get("location"),
                        "carrier": data.get("carrier"),
                        "line_type": data.get("line_type"),
                        "coordinates": {
                            "latitude": data.get("latitude"),
                            "longitude": data.get("longitude")
                        }
                    },
                    "reputation": {
                        "valid": data.get("valid", False),
                        "fraud_score": self._check_fraud_score(phone),
                        "spam_listings": self._check_spam_listings(phone)
                    }
                }
        except Exception as e:
            self.console.print(f"[red]Error in phone analysis: {str(e)}[/red]")
        return {"location": {}, "reputation": {}}

    def _query_whitepages(self, phone: str) -> Dict[str, Any]:
        """Query WhitePages Pro API for comprehensive phone information"""
        try:
            api_key = self.api_keys.get("whitepages")
            if not api_key:
                return {}

            headers = {
                "Api-Key": api_key,
                "Accept": "application/json"
            }
            
            response = requests.get(
                f"https://api.whitepages.com/3.0/phone",
                params={"phone": phone},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "owner_name": data.get("belongs_to", {}).get("name"),
                    "current_address": data.get("current_address"),
                    "historical_addresses": data.get("historical_addresses", []),
                    "associated_people": data.get("associated_people", []),
                    "phone_type": data.get("line_type"),
                    "carrier": data.get("carrier_name"),
                    "is_prepaid": data.get("is_prepaid"),
                    "is_commercial": data.get("is_commercial")
                }
        except Exception as e:
            self.console.print(f"[red]Error querying WhitePages: {str(e)}[/red]")
        return {}

    def _query_spokeo(self, phone: str) -> Dict[str, Any]:
        """Query Spokeo API for additional background information"""
        try:
            api_key = self.api_keys.get("spokeo")
            if not api_key:
                return {}

            headers = {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"https://api.spokeo.com/v1/phone/{phone}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "owner_details": data.get("owner", {}),
                    "location_history": data.get("locations", []),
                    "relatives": data.get("relatives", []),
                    "associates": data.get("associates", []),
                    "social_profiles": data.get("social_profiles", []),
                    "professional_records": data.get("professional_records", []),
                    "criminal_records": data.get("criminal_records", [])
                }
        except Exception as e:
            self.console.print(f"[red]Error querying Spokeo: {str(e)}[/red]")
        return {}

    def _check_fraud_score(self, phone: str) -> float:
        """Check phone number against fraud databases"""
        try:
            ipqs_key = self.api_keys.get("ipqualityscore")
            if not ipqs_key:
                return 0.0

            response = requests.get(
                "https://www.ipqualityscore.com/api/json/phone/",
                params={
                    "key": ipqs_key,
                    "phone": phone
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("fraud_score", 0.0)
        except Exception:
            pass
        return 0.0

    def _check_spam_listings(self, phone: str) -> List[Dict[str, Any]]:
        """Check phone number against spam databases"""
        spam_listings = []
        try:
            abuseipdb_key = self.api_keys.get("abuseipdb")
            if abuseipdb_key:
                response = requests.get(
                    "https://api.abuseipdb.com/api/v2/check-phone",
                    headers={"Key": abuseipdb_key},
                    params={"phone": phone}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data", {}).get("totalReports", 0) > 0:
                        spam_listings.append({
                            "source": "AbuseIPDB",
                            "reports": data["data"]["totalReports"],
                            "last_reported": data["data"].get("lastReportedAt")
                        })
        except Exception:
            pass
        return spam_listings

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
        try:
            api_key = self.api_keys.get("dehashed")
            if not api_key:
                return []

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json"
            }
            
            response = requests.get(
                "https://api.dehashed.com/search",
                params={"query": f"email:{email}"},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                breaches = []
                
                for entry in data.get("entries", []):
                    breaches.append({
                        "source": entry.get("database_name"),
                        "date": entry.get("obtained_date"),
                        "exposed_data": {
                            "username": entry.get("username"),
                            "password_hash": entry.get("hashed_password"),
                            "ip_address": entry.get("ip_address"),
                            "name": entry.get("name"),
                            "address": entry.get("address")
                        }
                    })
                return breaches
        except Exception as e:
            self.console.print(f"[red]Error querying DeHashed: {str(e)}[/red]")
        return []

    def _query_intelligence_x(self, email: str) -> Dict[str, Any]:
        """Query Intelligence X for email information"""
        try:
            api_key = self.api_keys.get("intelligence_x")
            if not api_key:
                return {"domain_info": {}}

            headers = {
                "x-key": api_key,
                "User-Agent": "OSINTScanner/1.0"
            }
            
            # Search for email in Intelligence X database
            search_response = requests.get(
                "https://intelx.io/intelligent/search",
                params={
                    "term": email,
                    "lookuplevel": 2,
                    "buckets": ["pastes", "darknet", "leaks"]
                },
                headers=headers
            )
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                results = {
                    "domain_info": {},
                    "leaks": [],
                    "darknet_mentions": [],
                    "paste_sites": []
                }
                
                # Get detailed information for each result
                for item in search_data.get("records", []):
                    record_response = requests.get(
                        f"https://intelx.io/intelligent/record/{item['id']}",
                        headers=headers
                    )
                    
                    if record_response.status_code == 200:
                        record = record_response.json()
                        
                        if record["type"] == "leak":
                            results["leaks"].append({
                                "title": record.get("title"),
                                "date": record.get("date"),
                                "source": record.get("source"),
                                "data_types": record.get("data_types", [])
                            })
                        elif record["type"] == "darknet":
                            results["darknet_mentions"].append({
                                "site": record.get("site"),
                                "date": record.get("date"),
                                "context": record.get("snippet")
                            })
                        elif record["type"] == "paste":
                            results["paste_sites"].append({
                                "site": record.get("site"),
                                "date": record.get("date"),
                                "title": record.get("title")
                            })
                
                return results
        except Exception as e:
            self.console.print(f"[red]Error querying Intelligence X: {str(e)}[/red]")
        return {"domain_info": {}}

    def _check_social_media(self, email: str) -> List[Dict[str, Any]]:
        """Check social media presence using various APIs"""
        social_profiles = []
        try:
            # FullContact API Integration
            fullcontact_key = self.api_keys.get("fullcontact")
            if fullcontact_key:
                headers = {
                    "Authorization": f"Bearer {fullcontact_key}"
                }
                response = requests.post(
                    "https://api.fullcontact.com/v3/person.enrich",
                    json={"email": email},
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for profile in data.get("socialProfiles", []):
                        social_profiles.append({
                            "platform": profile.get("type"),
                            "url": profile.get("url"),
                            "username": profile.get("username"),
                            "bio": profile.get("bio"),
                            "followers": profile.get("followers"),
                            "following": profile.get("following")
                        })
            
            # Additional social media checks using Maltego Transform
            maltego_key = self.api_keys.get("maltego")
            if maltego_key:
                headers = {
                    "Authorization": f"Bearer {maltego_key}"
                }
                response = requests.get(
                    "https://transforms.maltego.com/api/social-links",
                    params={"email": email},
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for profile in data.get("profiles", []):
                        if not any(p["url"] == profile["url"] for p in social_profiles):
                            social_profiles.append(profile)
                            
        except Exception as e:
            self.console.print(f"[red]Error checking social media: {str(e)}[/red]")
        return social_profiles

    def _analyze_email_pattern(self, email: str) -> Dict[str, Any]:
        """Analyze email pattern using various data enrichment services"""
        try:
            results = {
                "format_analysis": {},
                "domain_reputation": {},
                "similar_patterns": [],
                "associated_emails": []
            }
            
            # Email format analysis
            username, domain = email.split('@')
            results["format_analysis"] = {
                "pattern": self._detect_email_pattern(username),
                "common_format": self._is_common_format(username),
                "contains_numbers": any(c.isdigit() for c in username),
                "length": len(username)
            }
            
            # Domain reputation check using EmailRep
            emailrep_key = self.api_keys.get("emailrep")
            if emailrep_key:
                headers = {"Key": emailrep_key}
                response = requests.get(
                    f"https://emailrep.io/{email}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results["domain_reputation"] = {
                        "suspicious": data.get("suspicious"),
                        "disposable": data.get("details", {}).get("disposable"),
                        "deliverable": data.get("details", {}).get("deliverable"),
                        "spam": data.get("details", {}).get("spam"),
                        "free_provider": data.get("details", {}).get("free_provider"),
                        "days_since_domain_creation": data.get("details", {}).get("days_since_domain_creation"),
                        "profiles": data.get("details", {}).get("profiles", [])
                    }
            
            # Find similar patterns using Hunter.io
            hunter_key = self.api_keys.get("hunter")
            if hunter_key:
                response = requests.get(
                    "https://api.hunter.io/v2/domain-search",
                    params={
                        "domain": domain,
                        "api_key": hunter_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for email_data in data.get("data", {}).get("emails", []):
                        if email_data["value"] != email:  # Don't include the original email
                            results["associated_emails"].append({
                                "email": email_data["value"],
                                "type": email_data.get("type"),
                                "position": email_data.get("position"),
                                "department": email_data.get("department"),
                                "confidence_score": email_data.get("confidence")
                            })
                            
                            pattern = self._detect_email_pattern(email_data["value"].split('@')[0])
                            if pattern not in results["similar_patterns"]:
                                results["similar_patterns"].append(pattern)
            
            return results
            
        except Exception as e:
            self.console.print(f"[red]Error analyzing email pattern: {str(e)}[/red]")
            return {}

    def _detect_email_pattern(self, username: str) -> str:
        """Detect the pattern used in email username"""
        if '.' in username:
            parts = username.split('.')
            if len(parts) == 2:
                if len(parts[0]) == 1:
                    return "first_initial.lastname"
                return "firstname.lastname"
        elif '_' in username:
            return "separated_by_underscore"
        elif len(username) <= 3:
            return "initials"
        return "other"

    def _is_common_format(self, username: str) -> bool:
        """Check if username follows common corporate email formats"""
        common_patterns = [
            r'^[a-z]\.[a-z]+$',  # j.doe
            r'^[a-z]+\.[a-z]+$',  # john.doe
            r'^[a-z]{1,3}[0-9]{2,4}$',  # jd123
            r'^[a-z]+[0-9]{1,4}$'  # john123
        ]
        return any(re.match(pattern, username.lower()) for pattern in common_patterns)

    def _query_securitytrails(self, domain: str) -> List[Dict[str, Any]]:
        """Query SecurityTrails for domain history and infrastructure data"""
        try:
            api_key = self.api_keys.get("securitytrails")
            if not api_key:
                return []

            headers = {
                "APIKEY": api_key,
                "Accept": "application/json"
            }

            # Get historical DNS records
            response = requests.get(
                f"https://api.securitytrails.com/v1/history/{domain}/dns/a",
                headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                history = []
                
                for record in data.get("records", []):
                    history.append({
                        "first_seen": record.get("first_seen"),
                        "last_seen": record.get("last_seen"),
                        "ip_addresses": record.get("values", []),
                        "organization": record.get("organizations", []),
                        "type": "dns_a"
                    })

                # Get SSL certificate history
                ssl_response = requests.get(
                    f"https://api.securitytrails.com/v1/history/{domain}/ssl",
                    headers=headers
                )

                if ssl_response.status_code == 200:
                    ssl_data = ssl_response.json()
                    for cert in ssl_data.get("records", []):
                        history.append({
                            "first_seen": cert.get("first_seen"),
                            "last_seen": cert.get("last_seen"),
                            "issuer": cert.get("issuer", {}).get("name"),
                            "expires": cert.get("expires"),
                            "type": "ssl"
                        })

                return history
        except Exception as e:
            self.console.print(f"[red]Error querying SecurityTrails: {str(e)}[/red]")
        return []

    def _analyze_infrastructure(self, domain: str) -> Dict[str, Any]:
        """Analyze domain infrastructure using Censys and Shodan"""
        results = {}
        try:
            # Censys Analysis
            censys_key = self.api_keys.get("censys")
            if censys_key:
                headers = {
                    "Authorization": f"Bearer {censys_key}"
                }
                response = requests.get(
                    f"https://search.censys.io/api/v2/hosts/search",
                    params={"q": f"services.tls.certificates.leaf_data.names: {domain}"},
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results["censys"] = {
                        "open_ports": [],
                        "services": [],
                        "vulnerabilities": []
                    }
                    
                    for host in data.get("result", {}).get("hits", []):
                        results["censys"]["open_ports"].extend(host.get("services", []))
                        for service in host.get("services", []):
                            if service.get("vulnerabilities"):
                                results["censys"]["vulnerabilities"].extend(
                                    service["vulnerabilities"]
                                )

            # Shodan Analysis
            shodan_key = self.api_keys.get("shodan")
            if shodan_key:
                response = requests.get(
                    f"https://api.shodan.io/shodan/host/search",
                    params={
                        "key": shodan_key,
                        "query": f"hostname:{domain}"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results["shodan"] = {
                        "total_results": data.get("total", 0),
                        "hosts": []
                    }
                    
                    for match in data.get("matches", []):
                        results["shodan"]["hosts"].append({
                            "ip": match.get("ip_str"),
                            "ports": match.get("ports", []),
                            "vulns": match.get("vulns", []),
                            "tags": match.get("tags", []),
                            "hostnames": match.get("hostnames", [])
                        })

            return results
        except Exception as e:
            self.console.print(f"[red]Error analyzing infrastructure: {str(e)}[/red]")
        return {}

    def _analyze_dns(self, domain: str) -> Dict[str, Any]:
        """Analyze DNS records using various record types"""
        results = {
            "a_records": [],
            "mx_records": [],
            "ns_records": [],
            "txt_records": [],
            "spf_records": [],
            "dmarc_records": []
        }
        
        try:
            # A Records
            try:
                answers = dns.resolver.resolve(domain, 'A')
                for rdata in answers:
                    results["a_records"].append(str(rdata))
            except Exception:
                pass

            # MX Records
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                for rdata in answers:
                    results["mx_records"].append({
                        "preference": rdata.preference,
                        "exchange": str(rdata.exchange)
                    })
            except Exception:
                pass

            # NS Records
            try:
                answers = dns.resolver.resolve(domain, 'NS')
                for rdata in answers:
                    results["ns_records"].append(str(rdata))
            except Exception:
                pass

            # TXT Records
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    txt_string = b''.join(rdata.strings).decode()
                    results["txt_records"].append(txt_string)
                    
                    # Check for SPF records
                    if txt_string.startswith('v=spf1'):
                        results["spf_records"].append(txt_string)
            except Exception:
                pass

            # DMARC Record
            try:
                answers = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
                for rdata in answers:
                    dmarc_string = b''.join(rdata.strings).decode()
                    if dmarc_string.startswith('v=DMARC1'):
                        results["dmarc_records"].append(dmarc_string)
            except Exception:
                pass

            return results
        except Exception as e:
            self.console.print(f"[red]Error analyzing DNS records: {str(e)}[/red]")
        return results

    def _find_connected_domains(self, domain: str) -> List[str]:
        """Find connected domains using various intelligence sources"""
        connected_domains = set()
        try:
            # RiskIQ PassiveTotal
            riskiq_key = self.api_keys.get("riskiq")
            if riskiq_key:
                headers = {
                    "Authorization": f"Bearer {riskiq_key}"
                }
                response = requests.get(
                    f"https://api.riskiq.net/pt/v2/enrichment",
                    params={"query": domain},
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    connected_domains.update(data.get("subdomains", []))
                    connected_domains.update(data.get("related_domains", []))

            # DomainTools
            domaintools_key = self.api_keys.get("domaintools")
            if domaintools_key:
                headers = {
                    "Authorization": f"Bearer {domaintools_key}"
                }
                response = requests.get(
                    f"https://api.domaintools.com/v1/{domain}/related",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for domain_data in data.get("response", {}).get("domains", []):
                        connected_domains.add(domain_data.get("domain"))

            return list(connected_domains)
        except Exception as e:
            self.console.print(f"[red]Error finding connected domains: {str(e)}[/red]")
        return []

    def _query_threatcrowd(self, domain: str) -> Dict[str, Any]:
        """Query ThreatCrowd for domain intelligence"""
        try:
            response = requests.get(
                f"https://www.threatcrowd.org/searchApi/v2/domain/report/",
                params={"domain": domain}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "votes": data.get("votes", 0),
                    "references": data.get("references", []),
                    "resolutions": data.get("resolutions", []),
                    "subdomains": data.get("subdomains", []),
                    "emails": data.get("emails", []),
                    "hashes": data.get("hashes", [])
                }
        except Exception as e:
            self.console.print(f"[red]Error querying ThreatCrowd: {str(e)}[/red]")
        return {}

    def _query_wayback(self, domain: str) -> List[Dict[str, Any]]:
        """Query Wayback Machine for domain history"""
        try:
            response = requests.get(
                f"http://archive.org/wayback/available",
                params={"url": domain}
            )
            
            if response.status_code == 200:
                data = response.json()
                snapshots = []
                
                if "archived_snapshots" in data:
                    closest = data["archived_snapshots"].get("closest", {})
                    if closest:
                        snapshots.append({
                            "url": closest.get("url"),
                            "timestamp": closest.get("timestamp"),
                            "status": closest.get("status")
                        })
                        
                        # Get additional snapshots
                        cdx_response = requests.get(
                            "http://web.archive.org/cdx/search/cdx",
                            params={
                                "url": domain,
                                "output": "json",
                                "limit": 100
                            }
                        )
                        
                        if cdx_response.status_code == 200:
                            cdx_data = cdx_response.json()
                            if len(cdx_data) > 1:  # Skip header row
                                for row in cdx_data[1:]:
                                    snapshots.append({
                                        "timestamp": row[1],
                                        "original": row[2],
                                        "mimetype": row[3],
                                        "status": row[4],
                                        "digest": row[5]
                                    })
                
                return snapshots
        except Exception as e:
            self.console.print(f"[red]Error querying Wayback Machine: {str(e)}[/red]")
        return []

    def _query_blockchair(self, address: str) -> Dict[str, Any]:
        """Query Blockchair for crypto transaction history"""
        try:
            api_key = self.api_keys.get("blockchair")
            if not api_key:
                return {}

            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            
            # Get basic address information
            response = requests.get(
                f"https://api.blockchair.com/bitcoin/dashboards/address/{address}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                address_data = data.get("data", {}).get(address, {})
                
                return {
                    "balance": address_data.get("balance", 0),
                    "total_received": address_data.get("received", 0),
                    "total_sent": address_data.get("spent", 0),
                    "transaction_count": address_data.get("transaction_count", 0),
                    "first_seen": address_data.get("first_seen_in_block_time"),
                    "last_seen": address_data.get("last_seen_in_block_time"),
                    "unspent_outputs": address_data.get("unspent_output_count", 0)
                }
        except Exception as e:
            self.console.print(f"[red]Error querying Blockchair: {str(e)}[/red]")
        return {}

    def _analyze_wallet_cluster(self, address: str) -> Dict[str, Any]:
        """Analyze wallet clusters using GraphSense and WalletExplorer"""
        results = {
            "clusters": [],
            "known_entities": [],
            "risk_indicators": []
        }
        
        try:
            # GraphSense Analysis
            graphsense_key = self.api_keys.get("graphsense")
            if graphsense_key:
                headers = {
                    "Authorization": f"Bearer {graphsense_key}"
                }
                response = requests.get(
                    f"https://api.graphsense.info/bitcoin/addresses/{address}/clusters",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        for cluster in data:
                            results["clusters"].append({
                                "cluster_id": cluster.get("cluster"),
                                "size": cluster.get("size"),
                                "category": cluster.get("category"),
                                "first_activity": cluster.get("first_tx"),
                                "last_activity": cluster.get("last_tx"),
                                "total_received": cluster.get("total_received"),
                                "total_spent": cluster.get("total_spent")
                            })
            
            # WalletExplorer Analysis
            walletexplorer_key = self.api_keys.get("walletexplorer")
            if walletexplorer_key:
                response = requests.get(
                    "https://www.walletexplorer.com/api/1/address",
                    params={
                        "address": address,
                        "api_key": walletexplorer_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("wallet_name"):
                        results["known_entities"].append({
                            "name": data.get("wallet_name"),
                            "type": data.get("wallet_type"),
                            "first_seen": data.get("first_seen"),
                            "last_seen": data.get("last_seen")
                        })
            
            return results
        except Exception as e:
            self.console.print(f"[red]Error analyzing wallet clusters: {str(e)}[/red]")
        return {}

    def _query_bitcoinwhoswho(self, address: str) -> Dict[str, Any]:
        """Query BitcoinWhosWho for wallet intelligence"""
        default_response = {
            "scam_reports": [],
            "tags": [],
            "known_owner": {},
            "associated_sites": [],
            "risk_score": 0.1
        }
        try:
            api_key = self.api_keys.get("bitcoinwhoswho")
            if not api_key:
                return default_response

            headers = {
                "api-key": api_key
            }
            
            response = requests.get(
                f"https://bitcoinwhoswho.com/api/v1/address/{address}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "scam_reports": data.get("scam_reports", []),
                    "tags": data.get("tags", []),
                    "known_owner": data.get("owner_info", {}),
                    "associated_sites": data.get("websites", []),
                    "risk_score": data.get("risk_score", 0.1)
                }
            return default_response
        except Exception as e:
            self.console.print(f"[red]Error querying BitcoinWhosWho: {str(e)}[/red]")
        return {}

    def _analyze_eth_address(self, address: str) -> Dict[str, Any]:
        """Analyze Ethereum address using Ethplorer and Etherscan"""
        results = {
            "ethplorer": {
                "eth_balance": 0,
                "eth_total_in": 0,
                "eth_total_out": 0,
                "token_balances": [],
                "contract_info": {}
            },
            "etherscan": {
                "transactions": [],
                "internal_txs": [],
                "token_transfers": []
            }
        }
        
        try:
            # Ethplorer Analysis
            ethplorer_key = self.api_keys.get("ethplorer")
            if ethplorer_key:
                response = requests.get(
                    f"https://api.ethplorer.io/getAddressInfo/{address}",
                    params={"apiKey": ethplorer_key}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results["ethplorer"].update({
                        "eth_balance": data.get("ETH", {}).get("balance", 0),
                        "eth_total_in": data.get("ETH", {}).get("totalIn", 0),
                        "eth_total_out": data.get("ETH", {}).get("totalOut", 0),
                        "contract_info": data.get("contractInfo", {})
                    })
                    
                    for token in data.get("tokens", []):
                        results["ethplorer"]["token_balances"].append({
                            "token_name": token.get("tokenInfo", {}).get("name"),
                            "symbol": token.get("tokenInfo", {}).get("symbol"),
                            "balance": token.get("balance"),
                            "contract": token.get("tokenInfo", {}).get("address")
                        })
            
            # Etherscan Analysis
            etherscan_key = self.api_keys.get("etherscan")
            if etherscan_key:
                response = requests.get(
                    "https://api.etherscan.io/api",
                    params={
                        "module": "account",
                        "action": "txlist",
                        "address": address,
                        "apikey": etherscan_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results["etherscan"] = {
                        "transactions": [],
                        "internal_txs": [],
                        "token_transfers": []
                    }
                    
                    for tx in data.get("result", [])[:100]:  # Limit to last 100 transactions
                        results["etherscan"]["transactions"].append({
                            "hash": tx.get("hash"),
                            "timestamp": tx.get("timeStamp"),
                            "from": tx.get("from"),
                            "to": tx.get("to"),
                            "value": tx.get("value"),
                            "gas_used": tx.get("gasUsed")
                        })
            
            return results
        except Exception as e:
            self.console.print(f"[red]Error analyzing ETH address: {str(e)}[/red]")
        return {}

    def _generate_transaction_map(self, address: str) -> Dict[str, Any]:
        """Generate transaction map using Chainalysis and Breadcrumbs"""
        try:
            results = {
                "nodes": [],
                "edges": [],
                "clusters": [],
                "risk_flows": []
            }
            
            # Chainalysis Reactor API
            chainalysis_key = self.api_keys.get("chainalysis")
            if chainalysis_key:
                headers = {
                    "API-Key": chainalysis_key
                }
                response = requests.post(
                    "https://api.chainalysis.com/api/v1/address/exposure",
                    headers=headers,
                    json={"address": address}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results["risk_flows"] = data.get("risk_flows", [])
                    results["clusters"] = data.get("clusters", [])
            
            # Breadcrumbs Graph API
            breadcrumbs_key = self.api_keys.get("breadcrumbs")
            if breadcrumbs_key:
                headers = {
                    "Authorization": f"Bearer {breadcrumbs_key}"
                }
                response = requests.get(
                    f"https://api.breadcrumbs.app/v1/graphs/{address}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results["nodes"] = data.get("nodes", [])
                    results["edges"] = data.get("edges", [])
            
            return results
        except Exception as e:
            self.console.print(f"[red]Error generating transaction map: {str(e)}[/red]")
        return {}

    def _track_token_transactions(self, address: str) -> Dict[str, Any]:
        """Track token transactions using TokenView and Bloxy"""
        results = {
            "erc20_transfers": [],
            "nft_transfers": [],
            "token_holdings": []
        }
        
        try:
            # TokenView Analysis
            tokenview_key = self.api_keys.get("tokenview")
            if tokenview_key:
                headers = {
                    "api-key": tokenview_key
                }
                response = requests.get(
                    f"https://api.tokenview.com/v1/address/tokentxns/{address}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for tx in data.get("data", []):
                        tx_data = tx.copy()  # Create a copy to avoid modifying the original
                        if tx.get("tokenType") == "ERC20":
                            results["erc20_transfers"].append(tx_data)
                        elif tx.get("tokenType") in ["ERC721", "ERC1155"]:
                            results["nft_transfers"].append(tx_data)
            
            # Bloxy Token Analysis
            bloxy_key = self.api_keys.get("bloxy")
            if bloxy_key:
                response = requests.get(
                    "https://api.bloxy.info/address/token_balance_history",
                    params={
                        "address": address,
                        "key": bloxy_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results["token_holdings"].extend(data)
            
            return results
        except Exception as e:
            self.console.print(f"[red]Error tracking token transactions: {str(e)}[/red]")
        return {}

    def _is_eth_address(self, address: str) -> bool:
        """Check if address is a valid Ethereum address"""
        return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))
