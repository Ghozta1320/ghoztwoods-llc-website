import unittest
from osint_scanner import OSINTScanner
from unittest.mock import patch, MagicMock

class TestOSINTScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = OSINTScanner()
        
    def test_bitcoinwhoswho_with_no_api_key(self):
        """Test BitcoinWhosWho returns default response when no API key"""
        result = self.scanner._query_bitcoinwhoswho("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        expected = {
            "scam_reports": [],
            "tags": [],
            "known_owner": {},
            "associated_sites": [],
            "risk_score": 0.1
        }
        self.assertEqual(result, expected)
        
    @patch('requests.get')
    def test_bitcoinwhoswho_successful_response(self, mock_get):
        """Test BitcoinWhosWho successful API response handling"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "scam_reports": ["report1"],
            "tags": ["suspicious"],
            "owner_info": {"name": "test"},
            "websites": ["site1"],
            "risk_score": 0.8
        }
        mock_get.return_value = mock_response
        
        self.scanner.api_keys["bitcoinwhoswho"] = "test_key"
        result = self.scanner._query_bitcoinwhoswho("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        
        self.assertEqual(result["scam_reports"], ["report1"])
        self.assertEqual(result["risk_score"], 0.8)
        
    def test_eth_address_initialization(self):
        """Test Ethereum address analysis initialization"""
        result = self.scanner._analyze_eth_address("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        
        self.assertIn("ethplorer", result)
        self.assertIn("etherscan", result)
        self.assertEqual(result["ethplorer"]["eth_balance"], 0)
        self.assertEqual(len(result["etherscan"]["transactions"]), 0)
        
    @patch('requests.get')
    def test_eth_address_with_token_data(self, mock_get):
        """Test Ethereum address analysis with token data"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ETH": {"balance": 1.5, "totalIn": 2.0, "totalOut": 0.5},
            "tokens": [
                {
                    "tokenInfo": {
                        "name": "TestToken",
                        "symbol": "TST",
                        "address": "0x123"
                    },
                    "balance": "1000000000000000000"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        self.scanner.api_keys["ethplorer"] = "test_key"
        result = self.scanner._analyze_eth_address("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        
        self.assertEqual(result["ethplorer"]["eth_balance"], 1.5)
        self.assertEqual(len(result["ethplorer"]["token_balances"]), 1)
        
    def test_token_transactions_initialization(self):
        """Test token transactions tracking initialization"""
        result = self.scanner._track_token_transactions("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        
        self.assertIn("erc20_transfers", result)
        self.assertIn("nft_transfers", result)
        self.assertIn("token_holdings", result)
        self.assertEqual(len(result["erc20_transfers"]), 0)
        self.assertEqual(len(result["nft_transfers"]), 0)
        
    @patch('requests.get')
    def test_token_transactions_categorization(self, mock_get):
        """Test token transactions categorization"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"tokenType": "ERC20", "value": "100"},
                {"tokenType": "ERC721", "tokenId": "1"},
                {"tokenType": "ERC20", "value": "200"}
            ]
        }
        mock_get.return_value = mock_response
        
        self.scanner.api_keys["tokenview"] = "test_key"
        result = self.scanner._track_token_transactions("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        
        self.assertEqual(len(result["erc20_transfers"]), 2)
        self.assertEqual(len(result["nft_transfers"]), 1)

if __name__ == '__main__':
    unittest.main()
