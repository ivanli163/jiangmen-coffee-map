#!/bin/bash

# 部署辅助脚本
# 用于本地构建 Docker 镜像并推送到微信云托管

# 配置信息 (请修改此处)
# 您的环境 ID
ENV_ID="prod-9g8c363qb1f99532"
# 您的腾讯云镜像仓库地址 (请在云托管控制台查看)
# 格式通常为: ccr.ccs.tencentyun.com/tcb-<env_id>/<service_name>
IMAGE_REPO="ccr.ccs.tencentyun.com/tcb-prod-9g8c363qb1f99532/coffee-map"
# 镜像标签 (默认使用当前时间戳)
TAG=$(date +%Y%m%d%H%M%S)

echo "========================================"
echo "   江门咖啡地图 - 自动化部署脚本"
echo "========================================"
echo "环境 ID: $ENV_ID"
echo "镜像仓库: $IMAGE_REPO"
echo "本次标签: $TAG"
echo "========================================"

# 1. 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
  echo "❌ 错误: Docker 未运行，请先启动 Docker Desktop"
  exit 1
fi

# 2. 构建镜像
echo "🔨 正在构建 Docker 镜像..."
# 注意：这里使用 linux/amd64 平台，因为云托管通常运行在 Linux 服务器上
# 如果您的电脑是 M1/M2 Mac，不加 --platform linux/amd64 可能会导致部署后运行失败
docker build --platform linux/amd64 -t "$IMAGE_REPO:$TAG" -t "$IMAGE_REPO:latest" .

if [ $? -ne 0 ]; then
    echo "❌ 镜像构建失败"
    exit 1
fi

echo "✅ 镜像构建成功"

# 3. 登录腾讯云镜像仓库 (如果需要)
echo "🔑 请确认是否已登录腾讯云镜像仓库 (docker login ccr.ccs.tencentyun.com)"
read -p "是否需要执行登录操作? (y/n) " need_login
if [ "$need_login" = "y" ]; then
    echo "请输入腾讯云 Registry 用户名 (通常是账号ID):"
    read username
    echo "请输入密码:"
    read -s password
    echo "$password" | docker login ccr.ccs.tencentyun.com -u "$username" --password-stdin
fi

# 4. 推送镜像
echo "🚀 正在推送镜像到腾讯云..."
docker push "$IMAGE_REPO:$TAG"
docker push "$IMAGE_REPO:latest"

if [ $? -ne 0 ]; then
    echo "❌ 镜像推送失败"
    exit 1
else
    echo "✅ 镜像推送成功!"
    echo "----------------------------------------"
    echo "下一步:"
    echo "1. 打开微信云托管控制台: https://cloud.weixin.qq.com/"
    echo "2. 进入服务列表 -> 选择服务 -> 版本管理"
    echo "3. 如果开启了'镜像更新自动部署'，稍等片刻即可生效"
    echo "4. 否则，请手动点击'新建版本'，选择刚刚推送的标签: $TAG"
    echo "----------------------------------------"
fi
