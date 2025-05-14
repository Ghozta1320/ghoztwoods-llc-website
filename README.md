# Advanced Scam Detection & Protection System

A comprehensive web-based platform for protecting vulnerable populations from sophisticated scams, powered by advanced OSINT and threat intelligence capabilities.

## Features

### Enhanced Phone Intelligence
- Sync.me & PhoneInfoga integration for detailed carrier analysis
- WhitePages & Spokeo lookups for background information
- Advanced carrier and location tracking
- Real-time phone number validation and risk assessment

### Advanced Email Analysis
- DeHashed database integration for breach detection
- Intelligence X and Epieos OSINT tools
- Holehe social media presence checker
- Email format validation and verification
- Snov.io email pattern recognition

### Domain Reconnaissance
- SecurityTrails historical data analysis
- Censys and Shodan infrastructure scanning
- DNS Dumpster mapping
- SpyOnWeb connected domain detection
- ThreatCrowd intelligence gathering
- Wayback Machine history analysis

### Cryptocurrency Investigation
- Blockchair analytics integration
- WalletExplorer clustering
- BitcoinWhosWho intelligence
- Ethplorer and Bloxy analysis
- Breadcrumbs visualization
- TokenView transaction tracking

### Geolocation Tracking
- Multi-source location data aggregation
- Movement pattern analysis
- Anomaly detection
- Risk assessment based on location patterns

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Ghozta1320/Ghozta1320.github.io.git
cd Ghozta1320.github.io
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys:
Create a `config/api_keys.json` file with your API keys:
```json
{
    "dehashed": "your_key_here",
    "securitytrails": "your_key_here",
    "censys": "your_key_here",
    "shodan": "your_key_here",
    "etherscan": "your_key_here"
}
```

5. Start the API server:
```bash
python api.py
```

6. Open index.html in your browser to access the interface

## Usage

### Scanning Targets
1. Enter a target (phone, email, domain, or crypto address)
2. Select analysis type
3. View real-time results and risk assessment

### Submitting Tips
1. Navigate to the Contact page
2. Fill out the tip submission form
3. Include any relevant evidence or documentation

### Viewing Results
- Check the Analysis Results panel for detailed findings
- Review Risk Assessment scores
- Export detailed reports as needed

## API Endpoints

### `/api/scan`
- POST request
- Parameters:
  - target: string (required)
  - type: string (optional)
- Returns scan results and risk assessment

### `/api/submit-tip`
- POST request
- Parameters:
  - reporter_type: string
  - scam_type: string
  - details: object
- Returns tip submission confirmation

### `/api/phone-intel`
- POST request
- Parameters:
  - target: string (phone number)
- Returns detailed phone analysis

### `/api/email-analysis`
- POST request
- Parameters:
  - target: string (email address)
- Returns comprehensive email investigation

### `/api/domain-recon`
- POST request
- Parameters:
  - target: string (domain name)
- Returns domain intelligence

### `/api/crypto-investigation`
- POST request
- Parameters:
  - target: string (crypto address)
- Returns blockchain analysis

## Security Considerations

- All API keys should be kept secure
- Rate limiting is implemented on all endpoints
- Data is encrypted at rest and in transit
- User data is handled according to privacy regulations

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support or to report suspicious activity:
- Email: support@ghoztwoods.com
- Emergency Hotline: 1-800-XXX-XXXX

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ghoztwoods LLC for project support
- Partner agencies for collaboration
- Open-source intelligence community
