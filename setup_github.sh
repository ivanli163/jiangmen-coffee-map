#!/bin/bash

# GitHub 项目自动化设置脚本
# 用于检查环境、创建远程仓库并推送代码

GITHUB_USER="ivanli163"
REPO_NAME="jiangmen-coffee-map"
DESCRIPTION="江门咖啡地图 - 包含地图瓦片、后台管理系统及微信云托管部署配置"

echo "========================================"
echo "   GitHub 仓库自动化设置向导"
echo "========================================"

# 1. 检查 git 是否安装
if ! command -v git &> /dev/null; then
    echo "❌ 未找到 git 命令，请先安装 git。"
    exit 1
fi

# 2. 检查 git 用户配置
if [ -z "$(git config user.email)" ]; then
    echo "⚠️  未检测到 git 用户邮箱配置"
    echo "请输入您的 GitHub 邮箱:"
    read email
    git config --global user.email "$email"
fi

if [ -z "$(git config user.name)" ]; then
    echo "⚠️  未检测到 git 用户名配置"
    echo "请输入您的 GitHub 用户名 (例如 ivanli163):"
    read name
    git config --global user.name "$name"
fi

# 3. 智能获取 gh 工具
echo "🔍 检查 GitHub CLI 工具..."
GH_BIN="gh"

# 尝试查找本地下载的 gh
LOCAL_GH="./gh_2.62.0_macOS_arm64/bin/gh"
if [ -f "$LOCAL_GH" ]; then
    GH_BIN="$LOCAL_GH"
    echo "✅ 发现本地 GitHub CLI: $GH_BIN"
elif ! command -v gh &> /dev/null; then
    echo "⚠️  未找到系统安装的 gh 工具。"
    echo "⬇️  正在尝试为您下载独立的 GitHub CLI (无需 sudo 权限)..."
    
    # 下载 macOS arm64 版本 (根据之前 uname -m 结果)
    curl -L -O https://github.com/cli/cli/releases/download/v2.62.0/gh_2.62.0_macOS_arm64.zip
    
    if [ $? -eq 0 ]; then
        echo "📦 解压中..."
        unzip -o -q gh_2.62.0_macOS_arm64.zip
        
        if [ -f "$LOCAL_GH" ]; then
            GH_BIN="$LOCAL_GH"
            # 尝试移除 macOS 安全隔离属性 (Gatekeeper)
            xattr -d com.apple.quarantine "$GH_BIN" 2>/dev/null
            chmod +x "$GH_BIN"
            echo "✅ GitHub CLI 下载并配置成功!"
        else
            echo "❌ 解压失败或文件结构不匹配。"
            exit 1
        fi
    else
        echo "❌ 下载失败。"
        exit 1
    fi
else
    echo "✅ 发现系统已安装 gh"
fi

# 4. 检查 gh 登录状态
echo "🔍 检查 GitHub 登录状态..."
if ! "$GH_BIN" auth status &> /dev/null; then
    echo "⚠️  您尚未登录 GitHub CLI。"
    echo "正在启动登录流程，请按提示操作 (选择 GitHub.com -> HTTPS -> Login with a web browser)..."
    "$GH_BIN" auth login
    
    if [ $? -ne 0 ]; then
        echo "❌ 登录失败，请重试。"
        exit 1
    fi
fi

# 5. 创建远程仓库
echo "🚀 正在为您创建 GitHub 仓库: $GITHUB_USER/$REPO_NAME ..."

# 检查仓库是否已存在
if "$GH_BIN" repo view "$GITHUB_USER/$REPO_NAME" &> /dev/null; then
    echo "⚠️  仓库 $GITHUB_USER/$REPO_NAME 已存在。"
    echo "正在关联现有仓库..."
    if ! git remote | grep -q origin; then
        git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    else
        git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    fi
else
    # 创建新仓库
    # --source=. : 使用当前目录作为源码
    # --public : 公开仓库 (如果是私有请改为 --private)
    # --push : 创建后自动推送
    "$GH_BIN" repo create "$GITHUB_USER/$REPO_NAME" --public --source=. --remote=origin --push --description "$DESCRIPTION"
    
    if [ $? -eq 0 ]; then
        echo "✅ 仓库创建并推送成功!"
    else
        echo "❌ 仓库创建失败，请检查上方错误信息。"
        exit 1
    fi
fi

# 6. 设置默认分支并推送 (防止 gh repo create 推送失败的情况)
echo "📤 确保代码已推送到 main 分支..."
git branch -M main
git push -u origin main

echo "========================================"
echo "🎉 恭喜! 项目已成功托管到 GitHub"
echo "仓库地址: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "========================================"
