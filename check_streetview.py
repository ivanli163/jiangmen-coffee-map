import requests

AK = 'j47PtZPQsdP0gGDSaSq7j1Ur0Vea6OrU'
# 使用刚才获取的坐标 (经度, 纬度)
LNG = 113.065243
LAT = 22.629588

URL = 'http://api.map.baidu.com/panorama/v2'
params = {
    'ak': AK,
    'width': 512,
    'height': 256,
    'location': f'{LNG},{LAT}',
    'fov': 180,
    # 'pitch': 0
}

print(f"Testing URL: {URL}?ak={AK}&width=512&height=256&location={LNG},{LAT}&fov=180")

try:
    response = requests.get(URL, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.headers.get('Content-Type')}")
    
    # 如果是图片，说明成功
    if 'image' in response.headers.get('Content-Type', ''):
        print("Success! Got an image.")
        with open('test_streetview.jpg', 'wb') as f:
            f.write(response.content)
    else:
        print("Failed or JSON response:")
        print(response.text)

except Exception as e:
    print(f"Error: {e}")
