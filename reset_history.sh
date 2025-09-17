#!/bin/bash
# ⚠️ 使用前请确认你在仓库根目录，并且已经备份好代码！

# 远程仓库地址 (换成你自己的)
REMOTE_URL="git@github.com:longwenjun0/website.git"

echo "正在清空本地 Git 历史..."
rm -rf .git

echo "重新初始化仓库..."
git init

echo "添加远程仓库..."
git remote add origin "$REMOTE_URL"

echo "添加所有文件..."
git add .

echo "创建新的提交..."
git commit -m 'Initial commit (reset history)'

echo "推送到远程（覆盖历史）..."
git branch -M main
git push -f origin main

echo "✅ 历史已清空，只保留当前代码。"
