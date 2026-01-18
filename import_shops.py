import pandas as pd
import sqlite3
import random
import datetime

# 配置
EXCEL_FILE = 'jiangmen_coffee_shops.xlsx'
DB_PATH = 'server/database.db'

# 区域映射 (中文 -> ID)
REGION_MAP = {
    '蓬江区': 'pengjiang',
    '江海区': 'jianghai',
    '新会区': 'xinhui',
    '台山市': 'taishan',
    '开平市': 'kaiping',
    '鹤山市': 'heshan',
    '恩平市': 'enping'
}

# 默认图片库 (Unsplash)
PLACEHOLDER_IMAGES = [
    'https://images.unsplash.com/photo-1509042239860-f550ce710b93',
    'https://images.unsplash.com/photo-1497935586351-b67a49e012bf',
    'https://images.unsplash.com/photo-1525610553991-2bede1a236e2',
    'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd',
    'https://images.unsplash.com/photo-1554118811-1e0d58224f24',
    'https://images.unsplash.com/photo-1559925393-8be0ec4767c8',
    'https://images.unsplash.com/photo-1507133750069-bef72f3710f9',
    'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085',
    'https://images.unsplash.com/photo-1511920170033-f8396924c348',
    'https://images.unsplash.com/photo-1453614512568-c4024d13c247'
]

def init_missing_regions(cursor):
    """确保所有区域都存在"""
    existing = set(row[0] for row in cursor.execute("SELECT id FROM regions").fetchall())
    
    new_regions = []
    if 'taishan' not in existing: new_regions.append(('taishan', '台山市', 0, 0))
    if 'kaiping' not in existing: new_regions.append(('kaiping', '开平市', 0, 0))
    if 'heshan' not in existing: new_regions.append(('heshan', '鹤山市', 0, 0))
    if 'enping' not in existing: new_regions.append(('enping', '恩平市', 0, 0))
    
    if new_regions:
        cursor.executemany("INSERT INTO regions (id, name, coord_x, coord_y) VALUES (?, ?, ?, ?)", new_regions)
        print(f"Added {len(new_regions)} new regions.")

def run_import():
    print("Reading Excel...")
    df = pd.read_excel(EXCEL_FILE)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    init_missing_regions(cursor)
    
    print("Importing shops...")
    count = 0
    for _, row in df.iterrows():
        # 映射字段
        name = row.get('店铺名称')
        if not name: continue
        
        region_name = row.get('区域')
        region_id = REGION_MAP.get(region_name, 'pengjiang') # 默认蓬江
        
        # 检查是否已存在 (简单去重)
        exists = cursor.execute("SELECT id FROM shops WHERE name = ? AND address = ?", (name, row.get('地址'))).fetchone()
        if exists:
            continue
            
        img = random.choice(PLACEHOLDER_IMAGES)
        
        # 插入
        cursor.execute('''
            INSERT INTO shops (
                region_id, name, tag, rating, img, desc, address, 
                lat, lng, phone, price, open_hours, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            region_id,
            name,
            row.get('标签', '咖啡'),
            str(row.get('评分', '0.0')),
            img,
            f"评论数: {row.get('评论数', 0)}",
            row.get('地址'),
            row.get('纬度(BD09)'),
            row.get('经度(BD09)'),
            str(row.get('电话', '')),
            str(row.get('人均价格', '')),
            str(row.get('营业时间', '')),
            'baidu_import'
        ))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"Import completed! Added {count} new shops.")

if __name__ == '__main__':
    run_import()
