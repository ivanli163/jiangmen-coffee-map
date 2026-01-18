import requests
import json

AK = 'j47PtZPQsdP0gGDSaSq7j1Ur0Vea6OrU'
QUERY = '咖啡'
REGION = '蓬江区'
URL = 'http://api.map.baidu.com/place/v2/search'

params = {
    'query': QUERY,
    'region': REGION,
    'output': 'json',
    'ak': AK,
    'scope': 2, # 详细信息
    'page_size': 1,
    'page_num': 0
}

response = requests.get(URL, params=params)
data = response.json()

print(json.dumps(data, indent=4, ensure_ascii=False))
