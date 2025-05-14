import unittest
from unittest.mock import patch, MagicMock
from final_project.osint_scanner import OSINTScanner

class TestOSINTScannerPart2(unittest.TestCase):
    def setUp(self):
        self.scanner = OSINTScanner()
        self.scanner.api_keys = {
            "shodan": "test_key",
            "virustotal": "test_key",
            "securitytrails": "test_key",
            "chainalysis": "test_key",
            "elliptic": "test_key",
            "github": "test_key",
            "twitter": "test_key"
        }

    @patch('requests.get')
    def test_infrastructure_analysis(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "domains": ["domain1.com"],
            "ip_addresses": ["1.1.1.1"],
            "ssl_certificates": ["cert1"],
            "hosting_info": {"provider": "test_host"}
        }
        mock_get.return_value = mock_response

        result = self.scanner.analyze_infrastructure("test_target")
        self.assertIn("domains", result)
        self.assertIn("ip_addresses", result)
        self.assertIn("ssl_certificates", result)
        self.assertIn("hosting_info", result)

    @patch('requests.get')
    def test_social_media_analysis(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "profiles": {
                "twitter": {"username": "test_user", "followers": 100},
                "github": {"username": "test_dev", "repos": 10}
            },
            "activity_score": 0.8,
            "influence_metrics": {"engagement_rate": 0.15}
        }
        mock_get.return_value = mock_response

        result = self.scanner.analyze_social_presence("test_target")
        self.assertIn("profiles", result)
        self.assertIn("activities", result)
        self.assertIn("influence_metrics", result)

    @patch('requests.get')
    def test_financial_analysis(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "cryptocurrency": {
                "addresses": ["btc_addr1", "eth_addr1"],
                "total_value": 1000.0
            },
            "transactions": [
                {"hash": "tx1", "value": 500.0},
                {"hash": "tx2", "value": 500.0}
            ],
            "risk_assessment": {"score": 0.3}
        }
        mock_get.return_value = mock_response

        result = self.scanner.analyze_financial_data("test_target")
        self.assertIn("cryptocurrency", result)
        self.assertIn("transactions", result)
        self.assertIn("risk_assessment", result)
