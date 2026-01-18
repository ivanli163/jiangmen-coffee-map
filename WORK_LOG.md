# 江门咖啡地图项目开发工作总结 (2026-01-18)

## 1. 工作概览
本日主要完成了“江门咖啡地图”项目从本地开发环境到微信云托管（WeChat Cloud Hosting）的完整迁移与部署配置。解决了静态资源访问、图片存储与加载权限、自动化部署流程以及微信小程序真机调试配置等关键问题。

## 2. 核心问题解决

### 2.1 地图与后台访问修复
*   **问题**：访问 `/output_jiangmen/coffee_map.html` 报 404 错误，原静态文件结构不适应 Flask 应用架构。
*   **解决方案**：
    *   重构 Flask 路由，将地图页面移至模板目录，通过 `/` 或 `/map` 路由渲染。
    *   为后台管理页面配置 `/admin` 路由。
    *   **当前线上地址**：
        *   地图主页：`https://flask-5ou3-218844-6-1396725319.sh.run.tcloudbase.com/`
        *   后台管理：`https://flask-5ou3-218844-6-1396725319.sh.run.tcloudbase.com/admin`

### 2.2 图片加载与 COS 权限问题
*   **问题**：部署后商家图片不显示，直接访问腾讯云 COS 对象存储链接报 403 Forbidden（因防盗链或私有读权限）。
*   **解决方案**：
    *   在前端 (`map.html`, `admin.html`) 实现 `getImageUrl` 函数进行地址转换。
    *   **策略调整**：放弃前端直接访问私有读的 COS Bucket，改为通过 Flask 后端服务代理访问。
    *   代码逻辑：识别 `/server/uploads/` 路径，强制将其域名替换为线上运行的 Flask 服务地址，绕过直接访问 COS 的限制。

### 2.3 自动化部署搭建
*   **问题**：手动打包上传繁琐，且容易因环境差异导致“本地正常线上报错”的问题。
*   **解决方案**：
    *   **Git 仓库初始化**：配置 `.gitignore`，确保保留关键的 36MB 地图瓦片数据 (`output_jiangmen/`)，同时排除虚拟环境 (`venv/`)。
    *   **CI/CD 流水线**：创建 GitHub Actions 工作流 (`.github/workflows/deploy.yml`)，实现代码推送到 `main` 分支即自动构建 Docker 镜像并部署到微信云托管。
    *   **本地辅助脚本**：编写 `deploy.sh`，支持在本地进行跨平台 (`linux/amd64`) Docker 构建。
    *   **Docker 适配**：创建 `server/__init__.py` 解决 Python 包路径识别问题，优化 `.dockerignore` 减小镜像体积。

### 2.4 微信小程序真机调试配置
*   **问题**：点击“真机调试”超时，提示 AppID 不匹配；项目缺乏小程序前端结构。
*   **解决方案**：
    *   **修正配置**：更新 `project.config.json` 中的 AppID 为 `wx809276a900cd24ca`。
    *   **补全结构**：创建 `miniprogram/` 目录，包含 `app.json` 和页面文件。
    *   **Web-View 集成**：使用 `<web-view>` 组件直接加载云托管的 Flask 网页，实现小程序壳套用 Web 应用的架构。

## 3. 关键文件变更

| 文件路径 | 变更类型 | 说明 |
| :--- | :--- | :--- |
| [app.py](file:///Users/ivanli/Downloads/gdal2tiles/server/app.py) | 修改 | 增加静态文件路由，配置数据库初始化，优化图片服务逻辑 |
| [map.html](file:///Users/ivanli/Downloads/gdal2tiles/server/templates/map.html) | 修改 | 增加 `getImageUrl` 适配线上图片地址，优化地图交互 |
| [admin.html](file:///Users/ivanli/Downloads/gdal2tiles/server/templates/admin.html) | 修改 | 修复后台图片预览，适配线上环境 |
| [deploy.yml](file:///Users/ivanli/Downloads/gdal2tiles/.github/workflows/deploy.yml) | 新增 | GitHub Actions CI/CD 配置文件 |
| [project.config.json](file:///Users/ivanli/Downloads/gdal2tiles/project.config.json) | 修改 | 更新 AppID，配置小程序编译选项 |
| `miniprogram/` | 新增 | 小程序前端代码，包含 `web-view` 页面 |
| `.gitignore` / `.dockerignore` | 修改 | 优化文件包含规则，确保瓦片上传、排除垃圾文件 |

## 4. 后续维护建议
1.  **域名配置**：请务必在微信公众平台“开发设置”中配置业务域名 `flask-5ou3-218844-6-1396725319.sh.run.tcloudbase.com`，否则正式版小程序可能无法加载页面。
2.  **数据持久化**：目前使用 SQLite (`database.db`)，容器重建后数据可能会重置（如果未挂载云存储）。建议后续对接微信云托管的 MySQL 服务。
3.  **HTTPS 证书**：云托管自带 HTTPS，无需额外配置，但需确保证书不过期。

---
*文档生成时间：2026-01-18*
