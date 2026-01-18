import requests

URL = "http://127.0.0.1:8000/server/uploads/shops/shop_1.jpg"

try:
    resp = requests.get(URL)
    print(f"Status Code: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('Content-Type')}")
    print(f"Content-Length: {resp.headers.get('Content-Length')}")
    if resp.status_code != 200:
        print(f"Error Content: {resp.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
