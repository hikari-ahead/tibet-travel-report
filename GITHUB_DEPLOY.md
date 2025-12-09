# GitHub Pages 部署指南

## 📋 前置要求

- 已安装 Git
- 拥有 GitHub 账号
- 已配置 Git 用户信息

## 🚀 部署步骤

### 方法一：使用命令行（推荐）

#### 1. 初始化 Git 仓库

```bash
cd /Users/hellaflush/Documents/travel
git init
git add .
git commit -m "Initial commit: 西藏行程分析报告"
```

#### 2. 在 GitHub 上创建新仓库

1. 访问 https://github.com/new
2. 仓库名称：`tibet-travel-report`（或您喜欢的名称）
3. 描述：`西藏9日冬季探险环线 - 行程分析报告`
4. 选择 Public（公开，GitHub Pages 免费版需要公开仓库）
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

#### 3. 连接本地仓库到 GitHub

```bash
# 替换 YOUR_USERNAME 为您的 GitHub 用户名
# 替换 REPO_NAME 为您创建的仓库名称
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

#### 4. 启用 GitHub Pages

1. 访问您的仓库页面：`https://github.com/YOUR_USERNAME/REPO_NAME`
2. 点击 **Settings**（设置）
3. 在左侧菜单中找到 **Pages**
4. 在 **Source** 部分：
   - 选择 **Deploy from a branch**
   - Branch 选择 **main**
   - Folder 选择 **/ (root)**
5. 点击 **Save**
6. 等待几分钟，GitHub 会显示您的页面地址：
   - `https://YOUR_USERNAME.github.io/REPO_NAME/`

### 方法二：使用 GitHub Desktop（图形界面）

1. 下载并安装 [GitHub Desktop](https://desktop.github.com/)
2. 打开 GitHub Desktop
3. 点击 **File** → **Add Local Repository**
4. 选择 `/Users/hellaflush/Documents/travel` 文件夹
5. 点击 **Publish repository**
6. 输入仓库名称和描述
7. 勾选 **Keep this code private**（如果需要私有仓库，但 GitHub Pages 免费版需要公开）
8. 点击 **Publish Repository**
9. 在 GitHub 网站上启用 Pages（参考方法一的第4步）

## ✅ 验证部署

1. 访问您的 GitHub Pages 地址
2. 应该能看到完整的行程分析报告
3. 图表应该正常显示

## 🔄 更新内容

如果修改了报告内容，需要重新提交：

```bash
git add .
git commit -m "Update travel report"
git push
```

GitHub Pages 会自动更新（可能需要几分钟）。

## 📝 注意事项

1. **API 密钥安全**：`config.py` 文件已在 `.gitignore` 中，不会被上传
2. **文件大小**：Excel 文件较大，如果 GitHub 提示文件过大，可以考虑：
   - 删除 Excel 文件（HTML 报告已包含所有信息）
   - 或使用 Git LFS
3. **自定义域名**（可选）：可以在 Settings → Pages 中设置自定义域名

## 🐛 常见问题

### 问题1：页面显示 404
- 确保 `index.html` 文件在仓库根目录
- 检查 GitHub Pages 设置是否正确
- 等待几分钟让 GitHub 完成部署

### 问题2：图表不显示
- 检查浏览器控制台是否有错误
- 确保 Chart.js CDN 链接可访问
- 检查网络连接

### 问题3：样式丢失
- 确保所有 CSS 都在 HTML 文件中（当前是内联样式，应该没问题）
- 检查文件路径是否正确

## 📚 相关资源

- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [Git 官方文档](https://git-scm.com/doc)

