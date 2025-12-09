#!/bin/bash
# GitHub Pages 部署脚本

echo "🚀 开始部署到 GitHub Pages..."

# 检查是否已初始化 Git
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 添加文件到 Git..."
    git add .
    
    echo "💾 提交更改..."
    read -p "请输入提交信息 (默认: Update travel report): " commit_msg
    commit_msg=${commit_msg:-"Update travel report"}
    git commit -m "$commit_msg"
else
    echo "✅ 没有需要提交的更改"
fi

# 检查是否已设置远程仓库
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  尚未设置远程仓库"
    echo "请先执行以下命令："
    echo "  git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
    echo ""
    read -p "是否现在设置远程仓库？(y/n): " setup_remote
    if [ "$setup_remote" = "y" ]; then
        read -p "请输入 GitHub 仓库 URL: " repo_url
        git remote add origin "$repo_url"
    else
        echo "❌ 取消部署"
        exit 1
    fi
fi

# 推送到 GitHub
echo "📤 推送到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 下一步："
echo "1. 访问您的 GitHub 仓库"
echo "2. 进入 Settings → Pages"
echo "3. Source 选择 'Deploy from a branch'"
echo "4. Branch 选择 'main'，Folder 选择 '/'"
echo "5. 点击 Save"
echo ""
echo "🌐 您的页面将在几分钟后可用："
echo "   https://YOUR_USERNAME.github.io/REPO_NAME/"

