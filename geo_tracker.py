import requests
import json
import socket
from datetime import datetime
import os
import folium
import warnings
from requests.exceptions import RequestException
warnings.filterwarnings("ignore")

class GeoTracker:
    def __init__(self):
        self.tracking_history = []
        self.findings_dir = os.path.join("findings", "geo_tracking")
        os.makedirs(self.findings_dir, exist_ok=True)
        
        # Custom headers for API requests
        self.headers = {
            "User-Agent": "Shadow-Intel-Research/1.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5"
        }
        
        # API endpoints
        self.apis = {
            "ip-api": "http://ip-api.com/json/{}",
            "ipapi": "https://ipapi.co/{}/json/"
        }
        
    def track_target(self, identifier):
        """Main tracking method that coordinates all geolocation operations"""
        if not identifier:
            return {"error": "No identifier provided"}
            
        results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "identifier": identifier,
            "locations": {},
            "data_sources": {
                "online": [],
                "offline": ["local_database"]
            }
        }
        
        try:
            # Determine identifier type and track accordingly
            if self._is_ip(identifier):
                results["locations"]["ip"] = self._track_ip(identifier)
                if results["locations"]["ip"].get("coordinates"):
                    try:
                        results["map_path"] = self._generate_map(results["locations"])
                    except Exception as e:
                        results["map_error"] = str(e)
            elif self._is_phone(identifier):
                results["locations"]["phone"] = self._track_phone(identifier)
            elif self._is_device_id(identifier):
                results["locations"]["device"] = self._track_device(identifier)
                
            # Save results
            self._save_results(results)
            self.tracking_history.append(results)
            
        except Exception as e:
            results["error"] = str(e)
            
        return results
        
    def _is_ip(self, identifier):
        """Check if identifier is an IP address"""
        try:
            socket.inet_aton(identifier)
            return True
        except:
            return False
            
    def _is_phone(self, identifier):
        """Check if identifier is a phone number"""
        return identifier.replace("+", "").replace("-", "").isdigit()
            
    def _is_device_id(self, identifier):
        """Check if identifier is a device ID"""
        return identifier.startswith("DEV_") or identifier.startswith("MAC_")
        
    def _track_ip(self, ip):
        """Track location based on IP address with multiple fallbacks"""
        errors = []
        
        # Try ip-api.com first
        try:
            response = requests.get(
                self.apis["ip-api"].format(ip),
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "source": "ip-api.com",
                        "coordinates": (data.get("lat"), data.get("lon")),
                        "city": data.get("city"),
                        "region": data.get("regionName"),
                        "country": data.get("country"),
                        "isp": data.get("isp"),
                        "org": data.get("org"),
                        "as": data.get("as"),
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
        except RequestException as e:
            errors.append(f"ip-api.com error: {str(e)}")
            
        # Try ipapi.co as fallback
        try:
            response = requests.get(
                self.apis["ipapi"].format(ip),
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "source": "ipapi.co",
                    "coordinates": (data.get("latitude"), data.get("longitude")),
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country": data.get("country_name"),
                    "isp": data.get("org"),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        except RequestException as e:
            errors.append(f"ipapi.co error: {str(e)}")
            
        # If all services failed, return error details
        return {
            "error": "All geolocation services failed",
            "details": errors
        }
            
    def _track_phone(self, phone):
        """Track location based on phone number"""
        return {
            "source": "Phone Tracking",
            "status": "Service not implemented",
            "note": "Requires carrier integration"
        }
        
    def _track_device_id(self, device_id):
        """Track location based on device ID"""
        return {
            "source": "Device Tracking",
            "status": "Service not implemented",
            "note": "Requires device tracking service"
        }
        
    def _generate_map(self, locations):
        """Generate an HTML map with all tracked locations"""
        try:
            # Find first valid coordinates
            coordinates = None
            for loc in locations.values():
                if isinstance(loc, dict) and loc.get("coordinates"):
                    if all(isinstance(c, (int, float)) for c in loc["coordinates"]):
                        coordinates = loc["coordinates"]
                        break
                    
            if not coordinates:
                return None
                
            # Create map
            m = folium.Map(location=coordinates, zoom_start=10)
            
            # Add markers for each location
            for source, loc in locations.items():
                if isinstance(loc, dict) and loc.get("coordinates"):
                    if all(isinstance(c, (int, float)) for c in loc["coordinates"]):
                        popup_text = f"""
                        Source: {source}<br>
                        City: {loc.get('city', 'Unknown')}<br>
                        Region: {loc.get('region', 'Unknown')}<br>
                        Country: {loc.get('country', 'Unknown')}<br>
                        ISP: {loc.get('isp', 'Unknown')}<br>
                        Last Updated: {loc.get('last_updated', 'Unknown')}
                        """
                        
                        folium.Marker(
                            location=loc["coordinates"],
                            popup=popup_text,
                            icon=folium.Icon(color='red', icon='info-sign')
                        ).add_to(m)
            
            # Save map to findings directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            map_path = os.path.join(self.findings_dir, f"map_{timestamp}.html")
            m.save(map_path)
            return map_path
            
        except Exception as e:
            raise Exception(f"Map generation failed: {str(e)}")
            
    def _save_results(self, results):
        """Save tracking results to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.findings_dir, f"track_{timestamp}.json")
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            results["saved_to"] = filename
        except Exception as e:
            results["save_error"] = str(e)
            
    def get_tracking_history(self):
        """Get history of all tracking operations"""
        return self.tracking_history
        
    def clear_history(self):
        """Clear tracking history"""
        self.tracking_history = []
        return True

if __name__ == "__main__":
    tracker = GeoTracker()
    print("Geo Tracker initialized with IP-based tracking")
    print("Ready for tracking operations...")
