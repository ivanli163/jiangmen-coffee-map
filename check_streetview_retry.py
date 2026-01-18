import requests

AK = 'j47PtZPQsdP0gGDSaSq7j1Ur0Vea6OrU'
# 蓬江区某坐标 (御life coffee)
LAT = 22.629588
LNG = 113.065243

URL = 'http://api.map.baidu.com/panorama/v2'

def check_streetview():
    print(f"Checking Street View API for location {LAT}, {LNG}...")
    params = {
        'ak': AK,
        'width': 512,
        'height': 256,
        'location': f"{LNG},{LAT}",
        'fov': 180
    }
    
    resp = requests.get(URL, params=params)
    print(f"Status Code: {resp.status_code}")
    
    try:
        data = resp.json()
        print(f"JSON Response: {data}")
    except:
        print("Response is not JSON (likely an image).")
        # Save it to verify
        with open('streetview_test.jpg', 'wb') as f:
            f.write(resp.content)
        print("Saved image to streetview_test.jpg")

if __name__ == "__main__":
    check_streetview()
