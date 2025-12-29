#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书图片爬取工具
用于爬取小红书笔记中的图片并更新HTML文件
"""

import requests
import json
import re
import time
from urllib.parse import quote
import os

class XiaohongshuImageCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.xiaohongshu.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
    def search_notes(self, keyword, limit=5):
        """
        搜索小红书笔记
        """
        try:
            # 使用小红书搜索API（需要根据实际情况调整）
            search_url = f"https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
            
            params = {
                'keyword': keyword,
                'page': 1,
                'page_size': limit,
                'search_id': '',
                'sort': 'general',
                'note_type': 0,
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'items' in data['data']:
                    return data['data']['items']
        except Exception as e:
            print(f"搜索失败: {e}")
        
        return []
    
    def get_note_images(self, note_id):
        """
        获取笔记中的图片
        """
        try:
            note_url = f"https://edith.xiaohongshu.com/api/sns/web/v1/feed"
            params = {
                'source_note_id': note_id,
                'image_formats': 'jpg,webp,avif',
            }
            
            response = self.session.get(note_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'items' in data['data']:
                    note = data['data']['items'][0]
                    if 'note_card' in note and 'image_list' in note['note_card']:
                        images = []
                        for img in note['note_card']['image_list']:
                            # 获取高清图片URL
                            if 'url' in img:
                                img_url = img['url']
                                # 转换为高清URL
                                if 'sns-webpic' in img_url:
                                    img_url = img_url.replace('sns-webpic', 'sns-img')
                                images.append(img_url)
                        return images
        except Exception as e:
            print(f"获取图片失败: {e}")
        
        return []
    
    def crawl_images_by_keyword(self, keyword, max_images=5):
        """
        根据关键词爬取图片
        """
        print(f"正在搜索关键词: {keyword}")
        notes = self.search_notes(keyword, limit=max_images)
        
        all_images = []
        for note in notes:
            if 'id' in note:
                note_id = note['id']
                print(f"  获取笔记 {note_id} 的图片...")
                images = self.get_note_images(note_id)
                all_images.extend(images)
                time.sleep(1)  # 避免请求过快
        
        return all_images[:max_images]
    
    def get_images_for_attractions(self):
        """
        为各个景点获取图片
        """
        attractions = {
            "克拉美丽沙漠公园": [
                "克拉美丽沙漠公园 冬季",
                "克拉美丽沙漠公园 冬季 自驾",
                "克拉美丽沙漠公园 冬季 拍照",
                "克拉美丽沙漠公园 冬季 露营",
                "克拉美丽沙漠公园 冬季 旅行"
            ],
            "海上魔鬼城": [
                "海上魔鬼城 福海 冬季",
                "海上魔鬼城 冬季 拍照",
                "海上魔鬼城 冬季 雅丹",
                "海上魔鬼城 冬季 旅行",
                "福海 海上魔鬼城 冬季"
            ],
            "将军山滑雪场": [
                "阿勒泰 将军山滑雪场 冬季",
                "将军山滑雪场 冬季 滑雪",
                "将军山滑雪场 冬季 夜场",
                "将军山滑雪场 冬季 娱雪",
                "将军山滑雪场 冬季 攻略"
            ],
            "禾木村": [
                "禾木村 冬季",
                "禾木村 冬季 雪景",
                "禾木村 冬季 拍照",
                "禾木村 冬季 民宿",
                "禾木村 冬季 旅行"
            ],
            "禾木吉克普林滑雪场": [
                "禾木 吉克普林滑雪场 冬季",
                "吉克普林滑雪场 冬季 滑雪",
                "吉克普林滑雪场 冬季 粉雪",
                "吉克普林滑雪场 冬季 攻略",
                "禾木 吉克普林 冬季"
            ],
            "喀纳斯景区": [
                "喀纳斯 冬季",
                "喀纳斯 冬季 雪景",
                "喀纳斯 冬季 拍照",
                "喀纳斯 冬季 观鱼台",
                "喀纳斯 冬季 三湾"
            ],
            "白哈巴": [
                "白哈巴 冬季",
                "白哈巴 冬季 雪景",
                "白哈巴 冬季 拍照",
                "白哈巴 冬季 民宿",
                "白哈巴 冬季 旅行"
            ]
        }
        
        results = {}
        for attraction, keywords in attractions.items():
            print(f"\n正在获取 {attraction} 的图片...")
            images = []
            for keyword in keywords[:2]:  # 每个景点使用前2个关键词
                img_list = self.crawl_images_by_keyword(keyword, max_images=2)
                images.extend(img_list)
                time.sleep(2)  # 避免请求过快
            
            # 去重并限制数量
            images = list(dict.fromkeys(images))[:5]
            results[attraction] = images
            print(f"  获取到 {len(images)} 张图片")
        
        return results


def update_html_with_images(html_file, images_dict):
    """
    更新HTML文件中的图片URL
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 映射景点名称到HTML中的标识
    attraction_map = {
        "克拉美丽沙漠公园": "克拉美丽沙漠公园",
        "海上魔鬼城": "海上魔鬼城",
        "将军山滑雪场": "将军山滑雪场",
        "禾木村": "禾木村",
        "禾木吉克普林滑雪场": "禾木吉克普林滑雪场",
        "喀纳斯景区": "喀纳斯景区",
        "白哈巴": "白哈巴"
    }
    
    for attraction, images in images_dict.items():
        if not images:
            continue
        
        # 查找对应的图片区域
        pattern = rf'<h4>.*?{re.escape(attraction)}.*?</h4>.*?<div class="image-slider">(.*?)</div>'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # 构建新的图片HTML
            new_images_html = ""
            for i, img_url in enumerate(images[:5], 1):
                # 使用图片代理服务避免防盗链
                proxy_url = f"https://images.weserv.nl/?url={quote(img_url, safe='')}"
                new_images_html += f'''
                                    <div class="image-item" data-label="冬季实景" onclick="window.open('https://www.xiaohongshu.com/search_result?keyword={quote(attraction + " 冬季", safe="")}', '_blank')">
                                        <img src="{proxy_url}" alt="{attraction}冬季{i}" loading="lazy" onerror="this.src='https://via.placeholder.com/800x600/667eea/ffffff?text=图片加载失败'">
                                    </div>
                '''
            
            # 替换图片区域
            old_slider = match.group(1)
            content = content.replace(old_slider, new_images_html.strip())
            print(f"已更新 {attraction} 的图片")
    
    # 保存文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("\nHTML文件已更新！")


if __name__ == "__main__":
    print("=" * 50)
    print("小红书图片爬取工具")
    print("=" * 50)
    
    crawler = XiaohongshuImageCrawler()
    
    # 获取图片
    print("\n开始爬取图片...")
    images_dict = crawler.get_images_for_attractions()
    
    # 保存结果
    output_file = "xiaohongshu_images.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(images_dict, f, ensure_ascii=False, indent=2)
    print(f"\n图片URL已保存到 {output_file}")
    
    # 更新HTML
    html_file = "新疆冬季行程规划.html"
    if os.path.exists(html_file):
        print(f"\n正在更新 {html_file}...")
        update_html_with_images(html_file, images_dict)
    else:
        print(f"\n警告: 未找到 {html_file}，请确保文件存在")
