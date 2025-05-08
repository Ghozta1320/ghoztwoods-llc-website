import requests

def test_api():
    url = 'http://localhost:5000/api/scan'
    data = {
        'target': 'test@example.com',
        'type': 'full'
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    test_api()
