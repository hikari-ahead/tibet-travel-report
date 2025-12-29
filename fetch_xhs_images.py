#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书图片获取工具 - 使用第三方API服务
"""

import requests
import json
import re
import time
from urllib.parse import quote
import os

# 使用第三方API服务获取小红书图片
# 注意：这些API可能需要付费或有限制，请根据实际情况调整

class XHSImageFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
    
    def get_images_from_api(self, keyword, max_images=5):
        """
        使用第三方API获取小红书图片
        这里使用一个示例API，实际使用时需要替换为可用的API
        """
        images = []
        
        # 方法1: 使用小红书搜索页面的图片（需要解析HTML）
        try:
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={quote(keyword)}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                # 从HTML中提取图片URL
                # 小红书图片URL格式通常是: https://sns-img-qc.xhscdn.com/...
                img_pattern = r'https://sns-img[^"]+\.(?:jpg|jpeg|png|webp)'
                found_images = re.findall(img_pattern, response.text)
                
                # 去重并限制数量
                images = list(dict.fromkeys(found_images))[:max_images]
        except Exception as e:
            print(f"API方法1失败: {e}")
        
        # 如果方法1失败，尝试使用图片代理服务
        if not images:
            # 使用一些公开的图片搜索服务作为备选
            # 注意：这些是占位符，实际需要替换为真实的小红书图片URL
            print(f"  警告: 无法直接获取图片，请手动添加图片URL")
        
        return images
    
    def fetch_all_images(self):
        """
        为所有景点获取图片
        """
        attractions_keywords = {
            "克拉美丽沙漠公园": [
                "克拉美丽沙漠公园 冬季",
                "克拉美丽沙漠公园 冬季 自驾",
            ],
            "海上魔鬼城": [
                "海上魔鬼城 福海 冬季",
                "海上魔鬼城 冬季 拍照",
            ],
            "将军山滑雪场": [
                "阿勒泰 将军山滑雪场 冬季",
                "将军山滑雪场 冬季 滑雪",
            ],
            "禾木村": [
                "禾木村 冬季",
                "禾木村 冬季 雪景",
            ],
            "禾木吉克普林滑雪场": [
                "禾木 吉克普林滑雪场 冬季",
                "吉克普林滑雪场 冬季 滑雪",
            ],
            "喀纳斯景区": [
                "喀纳斯 冬季",
                "喀纳斯 冬季 雪景",
            ],
            "白哈巴": [
                "白哈巴 冬季",
                "白哈巴 冬季 雪景",
            ]
        }
        
        results = {}
        for attraction, keywords in attractions_keywords.items():
            print(f"正在获取 {attraction} 的图片...")
            all_images = []
            
            for keyword in keywords:
                images = self.get_images_from_api(keyword, max_images=3)
                all_images.extend(images)
                time.sleep(1)
            
            # 去重并限制为5张
            results[attraction] = list(dict.fromkeys(all_images))[:5]
            print(f"  获取到 {len(results[attraction])} 张图片")
        
        return results


def update_html_file(html_file, images_dict):
    """
    更新HTML文件中的图片
    由于小红书图片有防盗链，使用图片代理服务
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 图片代理服务（避免防盗链）
    proxy_services = [
        "https://images.weserv.nl/?url=",  # weserv.nl
        "https://api.52vmy.cn/api/img?url=",  # 备用代理
    ]
    
    for attraction, images in images_dict.items():
        if not images:
            continue
        
        # 查找图片区域
        # 匹配模式：找到景点标题后的第一个image-slider
        pattern = rf'(<h4>.*?{re.escape(attraction)}.*?</h4>.*?<div class="image-slider">)(.*?)(</div>)'
        
        def replace_images(match):
            header = match.group(1)
            old_content = match.group(2)
            footer = match.group(3)
            
            # 构建新的图片HTML
            new_images = []
            for i, img_url in enumerate(images[:5], 1):
                # 使用代理服务
                proxy_url = proxy_services[0] + quote(img_url, safe='')
                xhs_keyword = quote(f"{attraction} 冬季", safe='')
                new_images.append(f'''
                                    <div class="image-item" data-label="冬季实景" onclick="window.open('https://www.xiaohongshu.com/search_result?keyword={xhs_keyword}', '_blank')">
                                        <img src="{proxy_url}" alt="{attraction}冬季{i}" loading="lazy" onerror="this.onerror=null; this.src='https://via.placeholder.com/800x600/667eea/ffffff?text=图片加载失败，点击查看小红书'">
                                    </div>''')
            
            return header + '\n'.join(new_images) + footer
        
        content = re.sub(pattern, replace_images, content, flags=re.DOTALL)
        print(f"已更新 {attraction} 的图片")
    
    # 保存文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("\nHTML文件已更新！")


def manual_image_input():
    """
    手动输入图片URL的方法
    """
    print("\n" + "="*60)
    print("由于小红书API限制，建议手动添加图片URL")
    print("="*60)
    print("\n使用方法：")
    print("1. 在小红书APP中搜索对应景点的冬季关键词")
    print("2. 打开笔记，长按图片选择'复制图片链接'或'保存图片'")
    print("3. 将图片URL添加到下面的配置中")
    print("\n或者使用浏览器开发者工具：")
    print("1. 打开小红书网页版")
    print("2. 按F12打开开发者工具")
    print("3. 在Network标签中筛选图片请求")
    print("4. 找到图片URL（通常是sns-img-qc.xhscdn.com域名）")
    print("="*60)
    
    # 提供一个配置模板
    template = {
        "克拉美丽沙漠公园": [
            "https://sns-img-qc.xhscdn.com/xxx",  # 替换为实际URL
            "https://sns-img-qc.xhscdn.com/xxx",
            "https://sns-img-qc.xhscdn.com/xxx",
            "https://sns-img-qc.xhscdn.com/xxx",
            "https://sns-img-qc.xhscdn.com/xxx",
        ],
        # ... 其他景点
    }
    
    config_file = "xhs_images_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print(f"\n配置模板已保存到 {config_file}")
    print("请编辑此文件，填入实际的图片URL，然后重新运行脚本")


if __name__ == "__main__":
    print("=" * 60)
    print("小红书图片获取工具")
    print("=" * 60)
    
    html_file = "新疆冬季行程规划.html"
    
    # 检查是否有手动配置
    config_file = "xhs_images_config.json"
    if os.path.exists(config_file):
        print(f"\n发现配置文件 {config_file}，使用配置中的图片URL...")
        with open(config_file, 'r', encoding='utf-8') as f:
            images_dict = json.load(f)
        
        # 更新HTML
        update_html_file(html_file, images_dict)
    else:
        print("\n未找到配置文件，尝试自动获取...")
        print("注意：由于小红书反爬虫机制，自动获取可能失败")
        print("建议使用手动配置方法（见下方）\n")
        
        fetcher = XHSImageFetcher()
        images_dict = fetcher.fetch_all_images()
        
        # 保存结果
        output_file = "xhs_images_auto.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(images_dict, f, ensure_ascii=False, indent=2)
        print(f"\n自动获取结果已保存到 {output_file}")
        
        # 如果获取到图片，更新HTML
        if any(images_dict.values()):
            update_html_file(html_file, images_dict)
        else:
            print("\n自动获取失败，请使用手动方法")
            manual_image_input()
