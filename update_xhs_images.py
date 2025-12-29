#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML文件中的小红书图片
使用方法：
1. 编辑 xhs_images_config.json，填入真实的图片URL
2. 运行此脚本：python update_xhs_images.py
"""

import json
import re
import os
from urllib.parse import quote

def update_html_with_images(html_file, images_config):
    """
    使用配置文件中的图片URL更新HTML
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 图片代理服务（避免防盗链）
    # 使用多个代理服务作为备选
    proxy_base = "https://images.weserv.nl/?url="
    
    updated_count = 0
    
    for attraction, images in images_config.items():
        if not images or all('placeholder' in img for img in images):
            print(f"跳过 {attraction}（未配置图片URL）")
            continue
        
        # 查找对应的图片区域
        # 匹配景点标题后的image-slider区域
        pattern = rf'(<h4>.*?{re.escape(attraction)}.*?</h4>.*?<div class="gallery-label">.*?</div>.*?<div class="image-gallery">.*?<div class="image-slider">)(.*?)(</div>.*?<div class="image-note">)'
        
        def replace_slider(match):
            nonlocal updated_count
            header = match.group(1)
            old_slider_content = match.group(2)
            footer = match.group(3)
            
            # 构建新的图片HTML
            new_images_html = []
            valid_images = [img for img in images if img and 'placeholder' not in img]
            
            if not valid_images:
                return match.group(0)  # 如果没有有效图片，保持原样
            
            for i, img_url in enumerate(valid_images[:5], 1):
                # 使用代理服务避免防盗链
                proxy_url = proxy_base + quote(img_url, safe='')
                xhs_keyword = quote(f"{attraction} 冬季", safe='')
                
                new_images_html.append(f'''                                    <div class="image-item" data-label="冬季实景" onclick="window.open('https://www.xiaohongshu.com/search_result?keyword={xhs_keyword}', '_blank')">
                                        <img src="{proxy_url}" alt="{attraction}冬季{i}" loading="lazy" onerror="this.onerror=null; this.src='https://via.placeholder.com/800x600/667eea/ffffff?text=图片加载失败，点击查看小红书'; this.style.cursor='pointer';" style="cursor: pointer;">
                                    </div>''')
            
            updated_count += 1
            return header + '\n'.join(new_images_html) + footer
        
        content = re.sub(pattern, replace_slider, content, flags=re.DOTALL)
    
    # 保存文件
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ 成功更新 {updated_count} 个景点的图片！")
        return True
    else:
        print("\n⚠️  未找到有效的图片URL，请先编辑配置文件")
        return False


def get_image_urls_guide():
    """
    提供获取小红书图片URL的指南
    """
    guide = """
    ════════════════════════════════════════════════════════════
    如何获取小红书图片URL（三种方法）
    ════════════════════════════════════════════════════════════
    
    方法1：使用浏览器开发者工具（推荐）
    ────────────────────────────────────────────────────────────
    1. 打开小红书网页版：https://www.xiaohongshu.com
    2. 搜索景点关键词，例如："禾木村 冬季"
    3. 打开一篇笔记，按F12打开开发者工具
    4. 切换到 Network（网络）标签
    5. 刷新页面，在筛选器中输入 "img" 或 "xhscdn"
    6. 找到图片请求，右键 → Copy → Copy link address
    7. 图片URL格式通常是：https://sns-img-qc.xhscdn.com/...
    
    方法2：使用浏览器扩展
    ────────────────────────────────────────────────────────────
    1. 安装浏览器扩展（如：图片助手、Image Downloader）
    2. 在小红书页面右键选择扩展
    3. 批量下载或复制图片URL
    
    方法3：使用第三方工具
    ────────────────────────────────────────────────────────────
    1. 使用小红书笔记解析工具（如：小红书笔记下载器）
    2. 输入笔记链接，获取图片URL列表
    
    ════════════════════════════════════════════════════════════
    配置步骤：
    ════════════════════════════════════════════════════════════
    1. 打开 xhs_images_config.json 文件
    2. 将 placeholder 替换为真实的图片URL
    3. 每个景点至少配置3-5张图片
    4. 保存文件后运行：python update_xhs_images.py
    
    ════════════════════════════════════════════════════════════
    """
    print(guide)


if __name__ == "__main__":
    print("=" * 60)
    print("小红书图片更新工具")
    print("=" * 60)
    
    config_file = "xhs_images_config.json"
    html_file = "新疆冬季行程规划.html"
    
    # 检查文件是否存在
    if not os.path.exists(config_file):
        print(f"\n❌ 配置文件 {config_file} 不存在")
        print("正在创建配置文件模板...")
        # 创建默认配置
        default_config = {
            "克拉美丽沙漠公园": [],
            "海上魔鬼城": [],
            "将军山滑雪场": [],
            "禾木村": [],
            "禾木吉克普林滑雪场": [],
            "喀纳斯景区": [],
            "白哈巴": []
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        print(f"✅ 已创建配置文件 {config_file}")
        get_image_urls_guide()
        exit(0)
    
    if not os.path.exists(html_file):
        print(f"\n❌ HTML文件 {html_file} 不存在")
        exit(1)
    
    # 读取配置
    print(f"\n📖 读取配置文件 {config_file}...")
    with open(config_file, 'r', encoding='utf-8') as f:
        images_config = json.load(f)
    
    # 检查配置
    has_images = False
    for attraction, images in images_config.items():
        valid_images = [img for img in images if img and 'placeholder' not in img.lower()]
        if valid_images:
            has_images = True
            print(f"  ✅ {attraction}: {len(valid_images)} 张图片")
        else:
            print(f"  ⚠️  {attraction}: 未配置图片")
    
    if not has_images:
        print("\n⚠️  配置文件中没有有效的图片URL")
        get_image_urls_guide()
        exit(0)
    
    # 更新HTML
    print(f"\n🔄 正在更新 {html_file}...")
    success = update_html_with_images(html_file, images_config)
    
    if success:
        print("\n✨ 完成！请在浏览器中打开HTML文件查看效果")
    else:
        print("\n💡 提示：请按照上面的指南获取图片URL并更新配置文件")
