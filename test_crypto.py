import unittest
from unittest.mock import patch, MagicMock
from osint_scanner import OSINTScanner

class TestCryptoAnalysis(unittest.TestCase):
    def setUp(self):
        self.scanner = OSINTScanner()
        self.test_btc_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Bitcoin genesis address
        self.test_eth_address = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"  # Ethereum Foundation

    @patch('requests.get')
    def test_blockchair_query(self, mock_get):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa": {
                    "balance": 100000000,
                    "received": 100000000,
                    "spent": 0,
                    "transaction_count": 1,
                    "first_seen_in_block_time": "2009-01-03",
                    "last_seen_in_block_time": "2009-01-03"
                }
            }
        }
        mock_get.return_value = mock_response

        result = self.scanner._query_blockchair(self.test_btc_address)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["balance"], 100000000)
        self.assertEqual(result["transaction_count"], 1)

        # Test error handling
        mock_get.side_effect = Exception("API Error")
        result = self.scanner._query_blockchair(self.test_btc_address)
        self.assertEqual(result, {})

    @patch('requests.get')
    def test_wallet_cluster_analysis(self, mock_get):
        # Mock GraphSense response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "cluster": "123",
            "size": 100,
            "category": "exchange",
            "first_tx": "2020-01-01",
            "last_tx": "2023-01-01"
        }]
        mock_get.return_value = mock_response

        result = self.scanner._analyze_wallet_cluster(self.test_btc_address)
        
        self.assertIsInstance(result, dict)
        self.assertIn("clusters", result)
        self.assertIn("known_entities", result)
        self.assertEqual(len(result["clusters"]), 1)
        
        # Test error handling
        mock_get.side_effect = Exception("API Error")
        result = self.scanner._analyze_wallet_cluster(self.test_btc_address)
        self.assertEqual(result, {})

    @patch('requests.get')
    def test_bitcoinwhoswho_query(self, mock_get):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "scam_reports": [],
            "tags": ["exchange"],
            "owner_info": {"name": "Test Exchange"},
            "risk_score": 0.1
        }
        mock_get.return_value = mock_response

        result = self.scanner._query_bitcoinwhoswho(self.test_btc_address)
        
        self.assertIsInstance(result, dict)
        self.assertIn("scam_reports", result)
        self.assertIn("tags", result)
        self.assertEqual(result["risk_score"], 0.1)

        # Test error handling
        mock_get.side_effect = Exception("API Error")
        result = self.scanner._query_bitcoinwhoswho(self.test_btc_address)
        self.assertEqual(result, {})

    @patch('requests.get')
    def test_eth_address_analysis(self, mock_get):
        # Mock Ethplorer response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ETH": {
                "balance": 1000000000000000000,
                "totalIn": 2000000000000000000,
                "totalOut": 1000000000000000000
            },
            "tokens": [{
                "tokenInfo": {
                    "name": "Test Token",
                    "symbol": "TEST",
                    "address": "0x123"
                },
                "balance": 1000
            }]
        }
        mock_get.return_value = mock_response

        result = self.scanner._analyze_eth_address(self.test_eth_address)
        
        self.assertIsInstance(result, dict)
        self.assertIn("ethplorer", result)
        self.assertIn("token_balances", result["ethplorer"])
        
        # Test error handling
        mock_get.side_effect = Exception("API Error")
        result = self.scanner._analyze_eth_address(self.test_eth_address)
        self.assertEqual(result, {})

    @patch('requests.post')
    @patch('requests.get')
    def test_transaction_map_generation(self, mock_get, mock_post):
        # Mock Chainalysis response
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            "risk_flows": [{"type": "exchange", "amount": 1.0}],
            "clusters": [{"id": "123", "category": "exchange"}]
        }
        mock_post.return_value = mock_post_response

        # Mock Breadcrumbs response
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            "nodes": [{"id": "1", "type": "address"}],
            "edges": [{"source": "1", "target": "2"}]
        }
        mock_get.return_value = mock_get_response

        result = self.scanner._generate_transaction_map(self.test_btc_address)
        
        self.assertIsInstance(result, dict)
        self.assertIn("nodes", result)
        self.assertIn("edges", result)
        self.assertIn("risk_flows", result)
        
        # Test error handling
        mock_post.side_effect = Exception("API Error")
        mock_get.side_effect = Exception("API Error")
        result = self.scanner._generate_transaction_map(self.test_btc_address)
        self.assertEqual(result, {})

    @patch('requests.get')
    def test_token_transaction_tracking(self, mock_get):
        # Mock TokenView response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"tokenType": "ERC20", "value": "1000"},
                {"tokenType": "ERC721", "tokenId": "123"}
            ]
        }
        mock_get.return_value = mock_response

        result = self.scanner._track_token_transactions(self.test_eth_address)
        
        self.assertIsInstance(result, dict)
        self.assertIn("erc20_transfers", result)
        self.assertIn("nft_transfers", result)
        self.assertEqual(len(result["erc20_transfers"]), 1)
        self.assertEqual(len(result["nft_transfers"]), 1)
        
        # Test error handling
        mock_get.side_effect = Exception("API Error")
        result = self.scanner._track_token_transactions(self.test_eth_address)
        self.assertEqual(result, {})

    def test_eth_address_validation(self):
        # Test valid Ethereum address
        self.assertTrue(self.scanner._is_eth_address(self.test_eth_address))
        
        # Test invalid addresses
        self.assertFalse(self.scanner._is_eth_address("invalid_address"))
        self.assertFalse(self.scanner._is_eth_address(self.test_btc_address))
        self.assertFalse(self.scanner._is_eth_address("0x123"))  # Too short
        self.assertFalse(self.scanner._is_eth_address("0x" + "g" * 40))  # Invalid hex

    def test_analyze_crypto_integration(self):
        # Test the main analyze_crypto method
        with patch.multiple(self.scanner,
                          _query_blockchair=MagicMock(return_value={"balance": 100}),
                          _analyze_wallet_cluster=MagicMock(return_value={"clusters": []}),
                          _query_bitcoinwhoswho=MagicMock(return_value={"risk_score": 0.1}),
                          _analyze_eth_address=MagicMock(return_value={}),
                          _generate_transaction_map=MagicMock(return_value={}),
                          _track_token_transactions=MagicMock(return_value={})):
            
            result = self.scanner.analyze_crypto(self.test_btc_address)
            
            self.assertIsInstance(result, dict)
            self.assertIn("transaction_history", result)
            self.assertIn("wallet_analysis", result)
            self.assertIn("cluster_info", result)
            self.assertIn("risk_factors", result)

if __name__ == '__main__':
    unittest.main()
