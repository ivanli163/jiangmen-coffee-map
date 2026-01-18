#!/bin/bash

# 获取当前时间戳
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups/$TIMESTAMP"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份数据库
if [ -f "server/database.db" ]; then
    cp "server/database.db" "$BACKUP_DIR/database.db"
    echo "✅ 数据库已备份至 $BACKUP_DIR/database.db"
else
    echo "⚠️ 数据库文件不存在，跳过备份"
fi

# 备份上传的图片 (可选，如果图片很多可能占用空间)
# cp -r "server/uploads" "$BACKUP_DIR/uploads"

# 备份关键代码 (可选)
mkdir -p "$BACKUP_DIR/server"
cp server/app.py "$BACKUP_DIR/server/app.py"
cp server/templates/admin.html "$BACKUP_DIR/server/admin.html"
echo "✅ 关键代码已备份至 $BACKUP_DIR/server"

echo "🎉 备份完成！备份目录: $BACKUP_DIR"
