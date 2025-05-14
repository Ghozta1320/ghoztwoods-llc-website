import unittest
from unittest.mock import patch, MagicMock
from final_project.osint_scanner import OSINTScanner

class TestOSINTScannerPart3(unittest.TestCase):
    def setUp(self):
        self.scanner = OSINTScanner()
        self.scanner.api_keys = {
            "maxmind": "test_key",
            "maltego": "test_key",
            "sixgill": "test_key",
            "recordedfuture": "test_key",
            "crowdstrike": "test_key",
            "censys": "test_key"
        }

    @patch('requests.get')
    def test_geospatial_analysis(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "locations": [
                {"lat": 40.7128, "lon": -74.0060, "timestamp": "2024-01-01"},
                {"lat": 34.0522, "lon": -118.2437, "timestamp": "2024-01-02"}
            ],
            "movement_patterns": {
                "frequent_locations": ["New York", "Los Angeles"],
                "travel_frequency": "high"
            }
        }
        mock_get.return_value = mock_response

        result = self.scanner.analyze_geospatial("test_target")
        self.assertIn("locations", result)
        self.assertIn("movements", result)
        self.assertIn("patterns", result)

    @patch('requests.get')
    def test_network_analysis(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "network_map": {
                "nodes": ["ip1", "ip2", "ip3"],
                "connections": [("ip1", "ip2"), ("ip2", "ip3")]
            },
            "services": ["http", "https", "ftp"],
            "vulnerabilities": [
                {"cve": "CVE-2024-1234", "severity": "high"},
                {"cve": "CVE-2024-5678", "severity": "medium"}
            ]
        }
        mock_get.return_value = mock_response

        result = self.scanner.analyze_network("test_target")
        self.assertIn("network_map", result)
        self.assertIn("services", result)
        self.assertIn("vulnerabilities", result)

    @patch('requests.get')
    def test_comprehensive_scan(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "test_data": "test_value",
            "risk_score": 0.75,
            "confidence": 0.9
        }
        mock_get.return_value = mock_response

        result = self.scanner.comprehensive_scan("test_target")
        
        # Verify all components are present
        self.assertIn("scan_metadata", result)
        self.assertIn("dark_web_exposure", result)
        self.assertIn("threat_actor_analysis", result)
        self.assertIn("infrastructure_analysis", result)
        self.assertIn("social_media_presence", result)
        self.assertIn("financial_intelligence", result)
        self.assertIn("geospatial_analysis", result)
        self.assertIn("network_topology", result)
        self.assertIn("relationship_mapping", result)

        # Verify scan metadata
        self.assertIn("timestamp", result["scan_metadata"])
        self.assertEqual(result["scan_metadata"]["target"], "test_target")
        self.assertEqual(result["scan_metadata"]["scan_type"], "comprehensive")

    def test_api_error_handling(self):
        """Test API error handling with network failures"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("API Connection Error")
            
            # Test dark web analysis error handling
            result = self.scanner.analyze_dark_web("test_target")
            self.assertEqual(result["marketplace_mentions"], [])
            self.assertEqual(result["forum_activities"], {})
            
            # Test network analysis error handling
            result = self.scanner.analyze_network("test_target")
            self.assertEqual(result["services"], [])
            self.assertEqual(result["vulnerabilities"], [])

    def test_rate_limit_handling(self):
        """Test rate limit handling and backoff strategy"""
        with patch('time.sleep') as mock_sleep:
            # Test basic rate limiting
            self.scanner._rate_limit_check("test_api")
            mock_sleep.assert_called_once_with(1)
            
            # Reset mock and test multiple calls
            mock_sleep.reset_mock()
            for _ in range(3):
                self.scanner._rate_limit_check("test_api")
            self.assertEqual(mock_sleep.call_count, 3)

if __name__ == '__main__':
    unittest.main()
