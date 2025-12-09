#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成HTML静态展示页面
"""

import pandas as pd
import json

# 从Excel读取数据
excel_file = "西藏行程分析报告.xlsx"

# 读取详细行程数据
df = pd.read_excel(excel_file, sheet_name='详细行程')
summary_df = pd.read_excel(excel_file, sheet_name='汇总统计')

# 转换为字典列表
itinerary_data = df.to_dict('records')
summary_data = dict(zip(summary_df['统计项'], summary_df['数值']))

# 准备图表数据
days = [f"Day {i+1}" for i in range(len(itinerary_data))]
distances = [item['实际距离(km)'] for item in itinerary_data]
times = [item['实际时间(小时)'] for item in itinerary_data]
estimated_times = [item['估算时间(小时)'] for item in itinerary_data]
estimated_distances = [item['估算距离(km)'] for item in itinerary_data]

# 转换为JSON字符串（用于JavaScript）
days_json_str = json.dumps(days, ensure_ascii=False)
distances_json_str = json.dumps(distances, ensure_ascii=False)
times_json_str = json.dumps(times, ensure_ascii=False)
estimated_times_json_str = json.dumps(estimated_times, ensure_ascii=False)
estimated_distances_json_str = json.dumps(estimated_distances, ensure_ascii=False)

# 生成HTML
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>西藏9日冬季探险环线 - 行程分析报告</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .chart-container {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .itinerary-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .itinerary-table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .itinerary-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .itinerary-table td {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .itinerary-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .itinerary-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .risk-badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }}
        
        .risk-high {{
            background: #ff6b6b;
            color: white;
        }}
        
        .risk-medium {{
            background: #ffd93d;
            color: #333;
        }}
        
        .risk-low {{
            background: #6bcf7f;
            color: white;
        }}
        
        .recommendations {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .recommendation-item {{
            padding: 15px;
            margin: 10px 0;
            background: white;
            border-left: 4px solid #667eea;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .recommendation-item.important {{
            border-left-color: #ff6b6b;
            background: #fff5f5;
        }}
        
        .recommendation-item.strong {{
            border-left-color: #ffd93d;
            background: #fffbf0;
        }}
        
        .recommendation-title {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .recommendation-item.important .recommendation-title {{
            color: #ff6b6b;
        }}
        
        .recommendation-item.strong .recommendation-title {{
            color: #ff9800;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .difference-positive {{
            color: #6bcf7f;
            font-weight: 600;
        }}
        
        .difference-negative {{
            color: #ff6b6b;
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .itinerary-table {{
                font-size: 0.9em;
            }}
            
            .itinerary-table th,
            .itinerary-table td {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏔️ 西藏9日冬季探险环线</h1>
            <p>行程分析与可行性评估报告</p>
            <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">基于高德地图API实际路径规划数据</p>
        </div>
        
        <div class="content">
            <!-- 总体数据概览 -->
            <div class="section">
                <h2 class="section-title">📊 总体数据概览</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{summary_data['总天数']}</div>
                        <div class="stat-label">总行程天数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{summary_data['总实际距离(km)']:.1f}</div>
                        <div class="stat-label">总行程距离 (公里)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{summary_data['总实际时间(小时)']:.1f}</div>
                        <div class="stat-label">总行车时间 (小时)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{summary_data['平均每日距离(km)']:.1f}</div>
                        <div class="stat-label">平均每日距离 (公里)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{summary_data['平均每日时间(小时)']:.1f}</div>
                        <div class="stat-label">平均每日时间 (小时)</div>
                    </div>
                </div>
            </div>
            
            <!-- 图表分析 -->
            <div class="section">
                <h2 class="section-title">📈 数据分析图表</h2>
                <div class="chart-container">
                    <canvas id="distanceChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="timeChart"></canvas>
                </div>
            </div>
            
            <!-- 每日行程详情 -->
            <div class="section">
                <h2 class="section-title">🗺️ 每日行程详情</h2>
                <table class="itinerary-table">
                    <thead>
                        <tr>
                            <th>日期</th>
                            <th>行程路线</th>
                            <th>实际距离</th>
                            <th>实际时间</th>
                            <th>时间差异</th>
                            <th>活动安排</th>
                            <th>住宿</th>
                            <th>风险提示</th>
                        </tr>
                    </thead>
                    <tbody>
"""

# 添加每日行程数据
for item in itinerary_data:
    time_diff = item['时间差异(小时)']
    time_diff_class = 'difference-positive' if time_diff <= 0 else 'difference-negative'
    time_diff_str = f"{time_diff:+.1f}" if time_diff != 0 else "0"
    
    risk_badge = ""
    risk_text = item.get('风险提示', '') or ''
    if risk_text and isinstance(risk_text, str):
        if '误机' in risk_text or '通行风险' in risk_text or '超长' in risk_text or '15' in risk_text:
            risk_badge = f'<span class="risk-badge risk-high">⚠️ 高风险</span>'
        else:
            risk_badge = f'<span class="risk-badge risk-medium">⚠️ 注意</span>'
    
    html_content += f"""
                        <tr>
                            <td><strong>{item['日期']}</strong><br><small>{item['星期']}</small></td>
                            <td>{item['行程']}</td>
                            <td>{item['实际距离(km)']:.1f} km</td>
                            <td>{item['实际时间(小时)']:.1f} 小时</td>
                            <td class="{time_diff_class}">{time_diff_str} 小时</td>
                            <td>{item['活动安排']}</td>
                            <td>{item['住宿']}</td>
                            <td>{risk_text} {risk_badge}</td>
                        </tr>
    """

html_content += """
                    </tbody>
                </table>
            </div>
            
            <!-- 关键风险点 -->
            <div class="section">
                <h2 class="section-title">⚠️ 关键风险点分析</h2>
                <div class="recommendations">
"""

# 添加风险分析
risk_items = [item for item in itinerary_data if item.get('风险提示') and isinstance(item.get('风险提示'), str) and item['风险提示'].strip()]
for item in risk_items:
    html_content += f"""
                    <div class="recommendation-item important">
                        <div class="recommendation-title">Day {itinerary_data.index(item)+1} ({item['日期']} {item['星期']})</div>
                        <div><strong>行程:</strong> {item['行程']}</div>
                        <div><strong>实际时间:</strong> {item['实际时间(小时)']:.1f} 小时</div>
                        <div><strong>风险:</strong> {item['风险提示']}</div>
                    </div>
    """

html_content += """
                </div>
            </div>
            
            <!-- 优化建议 -->
            <div class="section">
                <h2 class="section-title">💡 优化建议</h2>
                <div class="recommendations">
                    <div class="recommendation-item important">
                        <div class="recommendation-title">🔴 必须执行的措施</div>
                        <div>1. <strong>将返程航班改签至12月31日</strong> - 这是最重要的建议，可以避免最后一天的误机风险</div>
                        <div>2. <strong>出发前确认墨脱通行状况</strong> - 联系当地司机或旅游局，确认扎墨公路是否开放</div>
                        <div>3. <strong>预留20-30%的缓冲时间</strong> - 特别是Day 2和Day 9，冬季路况可能影响实际行驶时间</div>
                    </div>
                    
                    <div class="recommendation-item strong">
                        <div class="recommendation-title">🟡 强烈建议的措施</div>
                        <div>1. <strong>准备备选路线方案</strong> - 如果墨脱无法通行，及时调整路线（Day 2: 林芝→波密→然乌湖）</div>
                        <div>2. <strong>Day 7尽早出发</strong> - 建议5:00-6:00出发，15.8小时往返行程需要充足时间，强烈建议拆分为两天</div>
                        <div>3. <strong>Day 9控制纳木措游览时间</strong> - 建议不超过2小时，确保有足够时间前往机场</div>
                    </div>
                    
                    <div class="recommendation-item">
                        <div class="recommendation-title">🟢 可选优化措施</div>
                        <div>1. 考虑在Day 5或Day 8增加半天休息时间，缓解疲劳</div>
                        <div>2. <strong>强烈建议将Day 7拆分为两天</strong> - 15.8小时的单日行程存在严重安全风险，建议拆分为：Day 7: 日喀则→佩枯措观景台→阿玛直米雪山（住当地），Day 8: 返回日喀则</div>
                        <div>3. 准备路餐，减少中途用餐时间，提高行程效率</div>
                    </div>
                </div>
            </div>
            
            <!-- 可行性评估 -->
            <div class="section">
                <h2 class="section-title">✅ 可行性综合评估</h2>
                <div class="recommendations">
                    <div class="recommendation-item">
                        <div class="recommendation-title">整体评分: 7.5/10 - 可行，但需谨慎规划</div>
                        <div style="margin-top: 15px;">
                            <p><strong>✅ 优势:</strong></p>
                            <ul style="margin-left: 20px; margin-top: 10px;">
                                <li>整体时间优化：实际总时间47.9小时，比原估算56小时节省约8小时</li>
                                <li>部分路段比预期轻松：Day 5、Day 6、Day 8实际时间均少于估算</li>
                                <li>路线规划合理：大部分路段都有高速公路或良好路况</li>
                            </ul>
                        </div>
                        <div style="margin-top: 15px;">
                            <p><strong>⚠️ 需要注意的问题:</strong></p>
                            <ul style="margin-left: 20px; margin-top: 10px;">
                                <li>Day 2实际时间超出估算：需要预留更多缓冲时间</li>
                                <li>冬季路况影响：高海拔地区冬季路况可能影响实际行驶时间</li>
                                <li>高海拔适应：需要时间适应高海拔环境，可能影响驾驶状态</li>
                            </ul>
                        </div>
                        <div style="margin-top: 15px;">
                            <p><strong>🎯 关键成功因素:</strong></p>
                            <ul style="margin-left: 20px; margin-top: 10px;">
                                <li>墨脱通行状况确认</li>
                                <li>返程航班时间调整</li>
                                <li>充分的缓冲时间预留</li>
                                <li>良好的身体状况和高原适应</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>报告生成时间: 2024年12月</p>
            <p style="margin-top: 10px; opacity: 0.8;">数据来源: 高德地图API | 分析工具版本: v1.0</p>
        </div>
    </div>
    
    <script>
        // 准备图表数据
        const days = """ + days_json_str + """;
        const distances = """ + distances_json_str + """;
        const times = """ + times_json_str + """;
        const estimatedDistances = """ + estimated_distances_json_str + """;
        const estimatedTimes = """ + estimated_times_json_str + """;
        
        // 等待DOM加载完成
        document.addEventListener('DOMContentLoaded', function() {
            // 距离对比图表
            const distanceCtx = document.getElementById('distanceChart');
            if (distanceCtx) {
                new Chart(distanceCtx.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: days,
                        datasets: [{
                            label: '实际距离 (km)',
                            data: distances,
                            backgroundColor: 'rgba(102, 126, 234, 0.8)',
                            borderColor: 'rgba(102, 126, 234, 1)',
                            borderWidth: 2
                        }, {
                            label: '估算距离 (km)',
                            data: estimatedDistances,
                            backgroundColor: 'rgba(200, 200, 200, 0.5)',
                            borderColor: 'rgba(200, 200, 200, 1)',
                            borderWidth: 2,
                            borderDash: [5, 5]
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: '每日行程距离对比',
                                font: {
                                    size: 18,
                                    weight: 'bold'
                                }
                            },
                            legend: {
                                display: true,
                                position: 'top'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: '距离 (公里)'
                                }
                            }
                        }
                    }
                });
            }
            
            // 时间对比图表
            const timeCtx = document.getElementById('timeChart');
            if (timeCtx) {
                new Chart(timeCtx.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: days,
                        datasets: [{
                            label: '实际时间 (小时)',
                            data: times,
                            borderColor: 'rgba(102, 126, 234, 1)',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4
                        }, {
                            label: '估算时间 (小时)',
                            data: estimatedTimes,
                            borderColor: 'rgba(200, 200, 200, 1)',
                            backgroundColor: 'rgba(200, 200, 200, 0.1)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: '每日行车时间对比',
                                font: {
                                    size: 18,
                                    weight: 'bold'
                                }
                            },
                            legend: {
                                display: true,
                                position: 'top'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: '时间 (小时)'
                                }
                            }
                        }
                    }
                });
            }
        });
    </script>
</body>
</html>
"""

# 保存HTML文件
with open('行程分析报告.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ HTML报告已生成: 行程分析报告.html")

