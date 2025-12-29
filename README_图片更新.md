# 小红书图片更新指南

## 快速开始

### 方法1：手动配置（推荐）

1. **获取小红书图片URL**
   - 打开小红书网页版：https://www.xiaohongshu.com
   - 搜索景点关键词（如："禾木村 冬季"）
   - 打开笔记，按 `F12` 打开开发者工具
   - 切换到 `Network` 标签，筛选 `img` 或 `xhscdn`
   - 找到图片请求，右键 → `Copy` → `Copy link address`
   - 图片URL格式：`https://sns-img-qc.xhscdn.com/...`

2. **编辑配置文件**
   - 打开 `xhs_images_config.json`
   - 将每个景点的 `placeholder` 替换为真实的图片URL
   - 每个景点至少配置3-5张图片

3. **运行更新脚本**
   ```bash
   python update_xhs_images.py
   ```

### 方法2：使用浏览器脚本（更简单）

1. **在小红书页面打开浏览器控制台**（F12）
2. **复制并运行以下脚本**：

```javascript
// 小红书图片URL提取脚本
(function() {
    const images = [];
    document.querySelectorAll('img').forEach(img => {
        const src = img.src || img.getAttribute('data-src');
        if (src && src.includes('xhscdn.com')) {
            // 获取高清图片URL
            let hdUrl = src;
            if (src.includes('thumbnail')) {
                hdUrl = src.replace(/thumbnail\/[^/]+\//, '');
            }
            if (!images.includes(hdUrl)) {
                images.push(hdUrl);
            }
        }
    });
    
    // 显示结果
    console.log('找到', images.length, '张图片：');
    images.forEach((url, i) => {
        console.log(`${i+1}. ${url}`);
    });
    
    // 复制到剪贴板
    const json = JSON.stringify(images, null, 2);
    navigator.clipboard.writeText(json).then(() => {
        console.log('✅ 图片URL已复制到剪贴板！');
        console.log('请粘贴到 xhs_images_config.json 文件中');
    });
    
    return images;
})();
```

3. **将复制的URL粘贴到配置文件中**

## 配置文件格式

```json
{
  "景点名称": [
    "https://sns-img-qc.xhscdn.com/图片1URL",
    "https://sns-img-qc.xhscdn.com/图片2URL",
    "https://sns-img-qc.xhscdn.com/图片3URL",
    "https://sns-img-qc.xhscdn.com/图片4URL",
    "https://sns-img-qc.xhscdn.com/图片5URL"
  ]
}
```

## 注意事项

1. **图片防盗链**：小红书图片有防盗链保护，脚本会自动使用代理服务
2. **图片数量**：每个景点建议配置5张图片
3. **图片质量**：尽量选择高清图片（URL中不包含 `thumbnail`）
4. **关键词搜索**：在小红书搜索时使用"景点名 + 冬季"关键词

## 景点列表

需要配置图片的景点：
- 克拉美丽沙漠公园
- 海上魔鬼城
- 将军山滑雪场
- 禾木村
- 禾木吉克普林滑雪场
- 喀纳斯景区
- 白哈巴

## 故障排除

### 图片无法显示
- 检查图片URL是否正确
- 确认URL格式：`https://sns-img-qc.xhscdn.com/...`
- 尝试在浏览器中直接打开URL测试

### 脚本运行失败
- 确认Python版本 >= 3.6
- 检查文件路径是否正确
- 确认HTML文件存在

### 需要帮助
- 查看 `update_xhs_images.py` 中的注释
- 检查控制台输出的错误信息
