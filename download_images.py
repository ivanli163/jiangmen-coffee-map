import os
import sqlite3
import requests
import time
from urllib.parse import urlparse

# 配置
DB_PATH = 'server/database.db'
SHOP_IMAGES_FOLDER = 'server/uploads/shops'

def download_images():
    # 确保目录存在
    if not os.path.exists(SHOP_IMAGES_FOLDER):
        os.makedirs(SHOP_IMAGES_FOLDER)
        print(f"Created directory: {SHOP_IMAGES_FOLDER}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取所有使用网络图片的商家
    cursor.execute("SELECT id, name, img FROM shops WHERE img LIKE 'http%'")
    shops = cursor.fetchall()
    
    print(f"Found {len(shops)} shops with remote images. Starting download...")
    
    count = 0
    for shop in shops:
        shop_id = shop[0]
        name = shop[1]
        img_url = shop[2]
        
        try:
            # 下载图片
            print(f"Downloading for shop {shop_id}: {name}...")
            response = requests.get(img_url, timeout=10)
            if response.status_code == 200:
                # 生成文件名
                filename = f"shop_{shop_id}.jpg"
                filepath = os.path.join(SHOP_IMAGES_FOLDER, filename)
                
                # 保存文件
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # 更新数据库
                local_url = f"/server/uploads/shops/{filename}"
                cursor.execute("UPDATE shops SET img = ? WHERE id = ?", (local_url, shop_id))
                conn.commit()
                count += 1
            else:
                print(f"Failed to download image for shop {shop_id}: Status {response.status_code}")
                
        except Exception as e:
            print(f"Error processing shop {shop_id}: {str(e)}")
            
        # 避免请求过快
        # time.sleep(0.1) 
        
    conn.close()
    print(f"Download completed. Updated {count} shops.")
    print(f"Images are saved in: {os.path.abspath(SHOP_IMAGES_FOLDER)}")

if __name__ == "__main__":
    download_images()
