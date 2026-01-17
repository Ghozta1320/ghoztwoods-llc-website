import requests
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import ipaddress
import geoip2.database
import socket
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from geopy.distance import geodesic

@dataclass
class LocationData:
    latitude: float
    longitude: float
    timestamp: datetime
    accuracy: float
    source: str
    confidence: float

class GeoTracker:
    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.geoip_reader = self._init_geoip_db()
        
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from configuration"""
        try:
            with open('config/api_keys.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _init_geoip_db(self):
        """Initialize GeoIP2 database reader"""
        try:
            return geoip2.database.Reader('data/GeoLite2-City.mmdb')
        except Exception:
            return None

    async def track_location(self, target: str) -> Dict[str, Any]:
        """Main method to track and analyze target location"""
        results = {
            "current_location": {},
            "historical_locations": [],
            "movement_patterns": {},
            "risk_assessment": {},
            "infrastructure_data": {},
            "correlation_data": []
        }

        try:
            # Get current location data
            current_loc = await self._get_current_location(target)
            results["current_location"] = current_loc

            # Get historical location data
            historical_data = await self._get_historical_locations(target)
            results["historical_locations"] = historical_data

            # Analyze movement patterns
            if historical_data:
                patterns = self._analyze_movement_patterns(historical_data)
                results["movement_patterns"] = patterns

            # Infrastructure analysis
            infra_data = await self._analyze_infrastructure(target)
            results["infrastructure_data"] = infra_data

            # Risk assessment
            risk_data = self._assess_location_risks(current_loc, historical_data)
            results["risk_assessment"] = risk_data

            # Correlation analysis
            if historical_data:
                correlations = self._analyze_correlations(historical_data)
                results["correlation_data"] = correlations

        except Exception as e:
            results["error"] = str(e)

        return results

    async def _get_current_location(self, target: str) -> Dict[str, Any]:
        """Get current location using multiple data sources"""
        location_data = {}

        try:
            # IP-based geolocation
            if self._is_ip(target):
                ip_loc = self._get_ip_location(target)
                if ip_loc:
                    location_data.update(ip_loc)

            # Cell tower triangulation (if phone number)
            if self._is_phone(target):
                cell_loc = await self._get_cell_location(target)
                if cell_loc:
                    location_data.update(cell_loc)

            # ISP data
            isp_data = await self._get_isp_data(target)
            if isp_data:
                location_data["isp_info"] = isp_data

            # VPN/Proxy detection
            proxy_data = self._check_proxy_usage(target)
            location_data["proxy_detection"] = proxy_data

        except Exception as e:
            location_data["error"] = str(e)

        return location_data

    async def _get_historical_locations(self, target: str) -> List[LocationData]:
        """Retrieve historical location data from multiple sources"""
        historical_data = []

        try:
            # Query various data sources
            dns_history = await self._get_dns_history(target)
            login_locations = await self._get_login_locations(target)
            social_media_locs = await self._get_social_media_locations(target)
            
            # Combine and normalize data
            all_locations = []
            all_locations.extend(self._normalize_locations(dns_history, "DNS"))
            all_locations.extend(self._normalize_locations(login_locations, "LOGIN"))
            all_locations.extend(self._normalize_locations(social_media_locs, "SOCIAL"))

            # Sort by timestamp
            historical_data = sorted(all_locations, key=lambda x: x.timestamp)

        except Exception as e:
            print(f"Error getting historical locations: {e}")

        return historical_data

    def _analyze_movement_patterns(self, locations: List[LocationData]) -> Dict[str, Any]:
        """Analyze movement patterns using machine learning"""
        patterns = {
            "clusters": [],
            "frequent_locations": [],
            "travel_patterns": [],
            "anomalies": []
        }

        try:
            if len(locations) < 2:
                return patterns

            # Convert locations to numpy array for clustering
            coords = np.array([[loc.latitude, loc.longitude] for loc in locations])
            
            # Perform DBSCAN clustering
            clustering = DBSCAN(eps=0.1, min_samples=2).fit(coords)
            
            # Analyze clusters
            unique_clusters = set(clustering.labels_)
            for cluster_id in unique_clusters:
                if cluster_id != -1:  # Ignore noise points
                    cluster_points = coords[clustering.labels_ == cluster_id]
                    center = cluster_points.mean(axis=0)
                    patterns["clusters"].append({
                        "center": center.tolist(),
                        "size": len(cluster_points)
                    })

            # Identify frequent locations
            for cluster in patterns["clusters"]:
                if cluster["size"] > len(locations) * 0.1:  # More than 10% of points
                    patterns["frequent_locations"].append(cluster)

            # Analyze travel patterns
            patterns["travel_patterns"] = self._analyze_travel(locations)

            # Detect anomalies
            patterns["anomalies"] = self._detect_location_anomalies(locations)

        except Exception as e:
            patterns["error"] = str(e)

        return patterns

    def _analyze_travel(self, locations: List[LocationData]) -> List[Dict[str, Any]]:
        """Analyze travel patterns between locations"""
        travel_patterns = []

        try:
            for i in range(len(locations) - 1):
                loc1, loc2 = locations[i], locations[i + 1]
                distance = geodesic(
                    (loc1.latitude, loc1.longitude),
                    (loc2.latitude, loc2.longitude)
                ).kilometers

                time_diff = (loc2.timestamp - loc1.timestamp).total_seconds() / 3600  # hours
                
                if distance > 0:
                    speed = distance / time_diff if time_diff > 0 else 0
                    
                    travel_patterns.append({
                        "start": {
                            "lat": loc1.latitude,
                            "lon": loc1.longitude,
                            "time": loc1.timestamp.isoformat()
                        },
                        "end": {
                            "lat": loc2.latitude,
                            "lon": loc2.longitude,
                            "time": loc2.timestamp.isoformat()
                        },
                        "distance_km": distance,
                        "duration_hours": time_diff,
                        "speed_kmh": speed
                    })

        except Exception as e:
            print(f"Error analyzing travel: {e}")

        return travel_patterns

    def _detect_location_anomalies(self, locations: List[LocationData]) -> List[Dict[str, Any]]:
        """Detect anomalous location patterns"""
        anomalies = []

        try:
            if len(locations) < 3:
                return anomalies

            # Calculate typical movement speeds
            speeds = []
            for i in range(len(locations) - 1):
                loc1, loc2 = locations[i], locations[i + 1]
                distance = geodesic(
                    (loc1.latitude, loc1.longitude),
                    (loc2.latitude, loc2.longitude)
                ).kilometers
                time_diff = (loc2.timestamp - loc1.timestamp).total_seconds() / 3600
                if time_diff > 0:
                    speeds.append(distance / time_diff)

            # Calculate speed statistics
            mean_speed = np.mean(speeds)
            std_speed = np.std(speeds)

            # Detect anomalies
            for i in range(len(locations) - 1):
                loc1, loc2 = locations[i], locations[i + 1]
                distance = geodesic(
                    (loc1.latitude, loc1.longitude),
                    (loc2.latitude, loc2.longitude)
                ).kilometers
                time_diff = (loc2.timestamp - loc1.timestamp).total_seconds() / 3600
                
                if time_diff > 0:
                    speed = distance / time_diff
                    if abs(speed - mean_speed) > 2 * std_speed:  # More than 2 standard deviations
                        anomalies.append({
                            "timestamp": loc2.timestamp.isoformat(),
                            "location": {
                                "lat": loc2.latitude,
                                "lon": loc2.longitude
                            },
                            "speed": speed,
                            "type": "Unusual speed",
                            "confidence": (abs(speed - mean_speed) / std_speed) if std_speed > 0 else 0
                        })

        except Exception as e:
            print(f"Error detecting anomalies: {e}")

        return anomalies

    def _assess_location_risks(self, current_loc: Dict[str, Any], 
                             historical_locs: List[LocationData]) -> Dict[str, Any]:
        """Assess risks based on location patterns"""
        risk_assessment = {
            "risk_score": 0.0,
            "risk_factors": [],
            "recommendations": []
        }

        try:
            # Check for VPN/Proxy usage
            if current_loc.get("proxy_detection", {}).get("is_proxy", False):
                risk_assessment["risk_factors"].append("VPN/Proxy detected")
                risk_assessment["risk_score"] += 0.3

            # Check for rapid location changes
            if historical_locs and len(historical_locs) > 1:
                for i in range(len(historical_locs) - 1):
                    loc1, loc2 = historical_locs[i], historical_locs[i + 1]
                    distance = geodesic(
                        (loc1.latitude, loc1.longitude),
                        (loc2.latitude, loc2.longitude)
                    ).kilometers
                    time_diff = (loc2.timestamp - loc1.timestamp).total_seconds() / 3600
                    
                    if time_diff > 0:
                        speed = distance / time_diff
                        if speed > 1000:  # Unrealistic speed
                            risk_assessment["risk_factors"].append("Suspicious location changes")
                            risk_assessment["risk_score"] += 0.2
                            break

            # Add recommendations based on risk factors
            if risk_assessment["risk_factors"]:
                risk_assessment["recommendations"].extend([
                    "Enable location verification",
                    "Monitor for unauthorized access",
                    "Review security settings"
                ])

        except Exception as e:
            risk_assessment["error"] = str(e)

        return risk_assessment

    def _is_ip(self, target: str) -> bool:
        """Check if target is an IP address"""
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            return False

    def _is_phone(self, target: str) -> bool:
        """Check if target is a phone number"""
        return bool(target and any(c.isdigit() for c in target))

    async def _get_cell_location(self, phone: str) -> Optional[Dict[str, Any]]:
        """Get location from cell tower data"""
        # Implementation for cell tower triangulation
        pass

    async def _get_isp_data(self, target: str) -> Optional[Dict[str, Any]]:
        """Get ISP information"""
        # Implementation for ISP data retrieval
        pass

    def _check_proxy_usage(self, target: str) -> Dict[str, bool]:
        """Check for VPN/Proxy usage"""
        # Implementation for proxy detection
        pass

    async def _get_dns_history(self, target: str) -> List[Dict[str, Any]]:
        """Get DNS history"""
        # Implementation for DNS history retrieval
        pass

    async def _get_login_locations(self, target: str) -> List[Dict[str, Any]]:
        """Get login location history"""
        # Implementation for login location retrieval
        pass

    async def _get_social_media_locations(self, target: str) -> List[Dict[str, Any]]:
        """Get locations from social media"""
        # Implementation for social media location retrieval
        pass

    def _normalize_locations(self, locations: List[Dict[str, Any]], 
                           source: str) -> List[LocationData]:
        """Normalize location data from different sources"""
        normalized = []
        
        for loc in locations:
            try:
                normalized.append(LocationData(
                    latitude=loc.get('latitude', 0.0),
                    longitude=loc.get('longitude', 0.0),
                    timestamp=datetime.fromisoformat(loc.get('timestamp', datetime.now().isoformat())),
                    accuracy=loc.get('accuracy', 0.0),
                    source=source,
                    confidence=loc.get('confidence', 0.0)
                ))
            except Exception as e:
                print(f"Error normalizing location: {e}")
                
        return normalized
