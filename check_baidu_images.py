import requests
import json

AK = 'j47PtZPQsdP0gGDSaSq7j1Ur0Vea6OrU'
QUERY = '咖啡'
REGION = '蓬江区'
URL_SEARCH = 'http://api.map.baidu.com/place/v2/search'
URL_DETAIL = 'http://api.map.baidu.com/place/v2/detail'

def check_images():
    print(f"Searching for '{QUERY}' in '{REGION}'...")
    
    # 1. Search API
    params = {
        'query': QUERY,
        'region': REGION,
        'output': 'json',
        'ak': AK,
        'scope': 2, # 详细信息
        'page_size': 1, # 先看一个
        'page_num': 0
    }
    
    try:
        resp = requests.get(URL_SEARCH, params=params)
        data = resp.json()
        
        if data.get('status') != 0:
            print(f"Error in Search API: {data.get('message')}")
            return

        results = data.get('results', [])
        if not results:
            print("No results found.")
            return

        first_poi = results[0]
        uid = first_poi.get('uid')
        name = first_poi.get('name')
        print(f"Found POI: {name} (UID: {uid})")
        
        # 打印 Search API 的 detail_info
        print("\n--- Search API 'detail_info' ---")
        print(json.dumps(first_poi.get('detail_info', {}), indent=4, ensure_ascii=False))
        
        # 2. Detail API
        if uid:
            print(f"\nFetching details for UID: {uid}...")
            detail_params = {
                'uid': uid,
                'output': 'json',
                'scope': 2,
                'ak': AK
            }
            detail_resp = requests.get(URL_DETAIL, params=detail_params)
            detail_data = detail_resp.json()
            
            if detail_data.get('status') == 0:
                result = detail_data.get('result', {})
                print("\n--- Detail API 'result' ---")
                # 打印所有一级 key，避免刷屏，但重点打印 detail_info
                print(f"Keys: {list(result.keys())}")
                print("Detail Info:")
                print(json.dumps(result.get('detail_info', {}), indent=4, ensure_ascii=False))
                
                # 检查是否有图片字段
                # 有时图片可能在 'images', 'content', 'rich_info' 等字段
            else:
                print(f"Error in Detail API: {detail_data.get('message')}")
                
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_images()
