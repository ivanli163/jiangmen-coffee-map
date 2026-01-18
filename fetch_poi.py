import requests
import pandas as pd
import time
import os

# 配置
AK = 'j47PtZPQsdP0gGDSaSq7j1Ur0Vea6OrU'
QUERY = '咖啡'
# 江门下辖区域
REGIONS = ['蓬江区', '江海区', '新会区', '台山市', '开平市', '鹤山市', '恩平市']

URL = 'http://api.map.baidu.com/place/v2/search'

def fetch_data():
    all_pois = []
    
    for region in REGIONS:
        print(f"正在获取 {region} 的数据...")
        page_num = 0
        while True:
            params = {
                'query': QUERY,
                'region': region,
                'output': 'json',
                'ak': AK,
                'scope': 2, # 2代表返回详细信息
                'page_size': 20,
                'page_num': page_num
            }
            
            try:
                response = requests.get(URL, params=params)
                data = response.json()
                
                if data['status'] != 0:
                    print(f"Error in {region} page {page_num}: {data.get('message')}")
                    break
                
                results = data.get('results', [])
                if not results:
                    print(f"  {region} 数据获取完毕")
                    break
                
                for poi in results:
                    # 提取基本信息
                    item = {
                        'name': poi.get('name'),
                        'address': poi.get('address'),
                        'bd09_lat': poi.get('location', {}).get('lat'), # 百度坐标纬度
                        'bd09_lng': poi.get('location', {}).get('lng'), # 百度坐标经度
                        'province': poi.get('province'),
                        'city': poi.get('city'),
                        'area': poi.get('area'),
                        'telephone': poi.get('telephone'),
                        'uid': poi.get('uid')
                    }
                    
                    # 提取详细信息 (Scope=2 时返回)
                    detail = poi.get('detail_info', {})
                    item['tag'] = detail.get('tag')
                    item['rating'] = detail.get('overall_rating')
                    item['price'] = detail.get('price')
                    item['shop_hours'] = detail.get('shop_hours')
                    item['image_num'] = detail.get('image_num')
                    item['comment_num'] = detail.get('comment_num')
                    item['detail_url'] = detail.get('detail_url')
                    
                    all_pois.append(item)
                
                print(f"  已获取 {region} 第 {page_num + 1} 页，本页 {len(results)} 条")
                page_num += 1
                time.sleep(0.2) # 礼貌延时
                
            except Exception as e:
                print(f"Request failed: {e}")
                break
                
    return all_pois

if __name__ == "__main__":
    print("开始爬取江门地区咖啡店数据...")
    pois = fetch_data()
    print(f"总共获取到 {len(pois)} 条数据")
    
    if pois:
        df = pd.DataFrame(pois)
        # 重命名列以更友好
        df.rename(columns={
            'name': '店铺名称',
            'address': '地址',
            'bd09_lat': '纬度(BD09)',
            'bd09_lng': '经度(BD09)',
            'province': '省份',
            'city': '城市',
            'area': '区域',
            'telephone': '电话',
            'tag': '标签',
            'rating': '评分',
            'price': '人均价格',
            'shop_hours': '营业时间',
            'comment_num': '评论数',
            'detail_url': '详情链接'
        }, inplace=True)
        
        output_file = 'jiangmen_coffee_shops.xlsx'
        df.to_excel(output_file, index=False)
        print(f"数据已成功保存到 {output_file}")
    else:
        print("未获取到任何数据，请检查API Key或网络。")
