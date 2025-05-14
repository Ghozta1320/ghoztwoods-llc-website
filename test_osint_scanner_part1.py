import unittest
from unittest.mock import patch, MagicMock
import json
from final_project.osint_scanner import OSINTScanner

class TestOSINTScannerPart1(unittest.TestCase):
    def setUp(self):
        self.scanner = OSINTScanner()
        self.scanner.api_keys = {
            "shodan": "test_key",
            "virustotal": "test_key",
            "securitytrails": "test_key",
            "chainalysis": "test_key",
            "elliptic": "test_key",
            "github": "test_key",
            "twitter": "test_key",
            "maxmind": "test_key",
            "maltego": "test_key",
            "sixgill": "test_key",
            "recordedfuture": "test_key",
            "crowdstrike": "test_key",
            "censys": "test_key"
        }

    @patch('requests.get')
    def test_dark_web_analysis(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "darkweb_mentions": ["forum_post_1", "marketplace_listing_1"],
            "risk_score": 0.75
        }
        mock_get.return_value = mock_response

        result = self.scanner.analyze_dark_web("test_target")
        self.assertIn("marketplace_mentions", result)
        self.assertIn("forum_activities", result)

    @patch('requests.get')
    def test_threat_actor_analysis(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "actors": ["threat_group_1"],
            "campaigns": ["campaign_1"]
        }
        mock_get.return_value = mock_response

        result = self.scanner.analyze_threat_actors("test_target")
        self.assertIn("known_actors", result)
        self.assertIn("attack_patterns", result)
