# 江门咖啡地图开发计划 5.0 (全链路集成版 - 静态视觉增强)

本项目是一个基于 Leaflet 和 gdal2tiles 的高性能 Web 地图应用，集成了微信小程序，旨在展示高清的江门咖啡文旅地图。项目采用“切片技术”解决 4K/8K 大图在移动端的加载性能问题，并实现了 Glassmorphism (玻璃拟态) UI 风格和深度的区域-商家联动交互。

## 1. 核心架构

### 1.1 技术栈
- **切片工具**: `gdal2tiles` (Python GDAL 库)
- **前端引擎**: Leaflet.js
- **UI 风格**: Glassmorphism (CSS3 Backdrop Filter)
- **移动端容器**: 微信小程序 `<web-view>`
- **服务端**: Python Flask (API + Static Files)
- **数据库**: SQLite
- **数据处理**: Pandas, OpenPyxl (Excel Import/Export)

### 1.2 目录结构
```
/Users/ivanli/Downloads/gdal2tiles/
├── server/
│   ├── app.py                 # [核心] Flask 后端应用 (API + 数据库)
│   ├── database.db            # SQLite 数据库文件 (自动生成)
│   ├── templates/
│       └── admin.html         # [新增] 商家管理后台 CMS
│   └── uploads/               # 本地图片存储
├── start_server.py            # (已废弃) 请使用 server/app.py
├── backup.sh                  # 数据备份脚本
├── ...
```

## 2. 图片切片与瓦片服务

### 2.1 切片命令
我们使用以下命令将 4K 竖版地图 (`3584x4800`) 切割为 0-5 级的瓦片：

```bash
gdal2tiles.py -p raster -z 0-5 --xyz --webviewer=leaflet "江门·邑啡冲煮-全域文旅地图-4K高清-简体中文.png" output_jiangmen
```

- **`-p raster`**: 适用于非地理坐标的普通图片。
- **`--xyz`**: 生成标准 XYZ 瓦片（原点左上角），避免坐标翻转问题。
- **`-z 0-5`**: 生成 6 个缩放层级。

### 2.2 坐标系说明
前端使用 `L.CRS.Simple` 平面坐标系：
- **原点 (0,0)**: 左下角 (Leaflet 默认逻辑) -> 通过 `map.unproject` 映射到像素坐标。
- **图片尺寸**: 宽 3584px, 高 4800px。

## 3. 功能特性 (Version 5.0)

### 3.1 视觉增强
- **暗黑模式**: 适配咖啡文化的深色调背景。
- **玻璃拟态**: 底部滑块和详情页采用半透明磨砂效果 (`backdrop-filter: blur(20px)`).
- **呼吸灯光标**: 重点区域（蓬江、江海、新会）使用 CSS 动画呼吸点标记。

### 3.2 深度交互
1.  **区域引导**: 点击地图上的“区域名称” (如蓬江区)。
2.  **自动聚焦**: 地图自动平滑飞行 (`flyTo`) 至该区域中心。
3.  **底部滑块**: 屏幕底部弹出该区域的商家列表（横向滚动）。
4.  **沉浸详情**: 点击商家卡片，全屏弹出高清图文详情页。

## 4. 快速开始

### 4.1 启动服务
在项目根目录运行：
```bash
python3 start_server.py
```
服务将启动在 `http://0.0.0.0:8000`。

### 4.2 访问地图
- **PC/手机浏览器**: 访问 `http://<本机IP>:8000/output_jiangmen/coffee_map.html`
- **微信小程序**: 使用微信开发者工具导入 `wechat_mp_demo` 目录，编译运行即可。
  - *注意*: 小程序代码中的 IP 地址已自动配置为本机 IP，如网络环境变化需更新。

## 5. 变更日志
- **v5.0 (Current)**: 集成 Glassmorphism UI，实现区域-商家二级联动，适配 4K 竖版地图。
- **v2.0 (Archived)**: 动效演示版 (已移除独立入口，功能合并至 5.0)。
- **v1.0**: 基础底图切片展示。

## 6. 版本管理与回滚指南
为确保系统稳定性，建议在进行重大更新前执行以下操作：

1.  **代码版本控制**: 建议使用 Git 初始化仓库 (`git init`) 并提交代码。
2.  **数据备份**:
    - 运行 `./backup.sh` 脚本。
    - 脚本会自动备份 `server/database.db` 和关键代码文件至 `backups/` 目录。
3.  **回滚操作**:
    - 如果更新后出现问题，将 `backups/` 目录下对应时间戳的 `database.db` 覆盖回 `server/` 目录。
    - 代码回滚建议使用 Git (`git checkout .` 或 `git revert`)。
