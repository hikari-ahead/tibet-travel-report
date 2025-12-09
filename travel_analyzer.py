#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西藏行程分析工具
使用高德地图API计算实际行车时间并生成报表
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from config import AMAP_API_KEY, AMAP_API_BASE_URL, AMAP_GEOCODE_URL


# 行程数据定义
ITINERARY = [
    {
        "day": 1,
        "date": "2024-12-22",
        "weekday": "周日",
        "route": "林芝米林机场 → 林芝市区",
        "origin": "林芝米林机场",
        "destination": "林芝八一镇",
        "estimated_distance": 50,
        "estimated_time": 1,
        "activities": "接机，寻找天空之树",
        "accommodation": "林芝八一镇"
    },
    {
        "day": 2,
        "date": "2024-12-23",
        "weekday": "周一",
        "route": "林芝 → 色季拉山口 → 波密 → 墨脱",
        "origin": "林芝八一镇",
        "destination": "墨脱县城",
        "waypoints": ["色季拉山口", "波密县城"],
        "estimated_distance": 250,
        "estimated_time": 6,
        "activities": "观南迦巴瓦峰，穿越鲁朗林海，进入墨脱",
        "accommodation": "墨脱县城",
        "risk": "扎墨公路通行风险"
    },
    {
        "day": 3,
        "date": "2024-12-24",
        "weekday": "周二",
        "route": "墨脱 → 波密 → 然乌湖",
        "origin": "墨脱县城",
        "destination": "然乌镇",
        "waypoints": ["波密县城"],
        "estimated_distance": 200,
        "estimated_time": 5,
        "activities": "墨脱热带雨林，然乌湖日落",
        "accommodation": "然乌镇"
    },
    {
        "day": 4,
        "date": "2024-12-25",
        "weekday": "周三",
        "route": "然乌湖 → 来古冰川 → 波密 → 林芝",
        "origin": "然乌镇",
        "destination": "林芝八一镇",
        "waypoints": ["来古冰川", "波密县城"],
        "estimated_distance": 360,
        "estimated_time": 7,
        "activities": "然乌湖晨景，来古冰川深度游",
        "accommodation": "林芝八一镇"
    },
    {
        "day": 5,
        "date": "2024-12-26",
        "weekday": "周四",
        "route": "林芝 → 拉萨",
        "origin": "林芝八一镇",
        "destination": "拉萨市",
        "estimated_distance": 400,
        "estimated_time": 5,
        "activities": "缓冲日，布达拉宫广场",
        "accommodation": "拉萨市"
    },
    {
        "day": 6,
        "date": "2024-12-27",
        "weekday": "周五",
        "route": "拉萨 → 羊卓雍措 → 卡若拉冰川 → 日喀则",
        "origin": "拉萨市",
        "destination": "日喀则市",
        "waypoints": ["羊卓雍措", "卡若拉冰川"],
        "estimated_distance": 350,
        "estimated_time": 7,
        "activities": "羊卓雍措全天游览",
        "accommodation": "日喀则市"
    },
    {
        "day": 7,
        "date": "2024-12-28",
        "weekday": "周六",
        "route": "日喀则 → 佩枯措观景台 → 阿玛直米雪山 → 日喀则",
        "origin": "西藏自治区日喀则市",
        "destination": "西藏自治区日喀则市",
        "waypoints": ["佩枯措观景台", "阿玛直米雪山"],
        "waypoint_coords": ["85.493658,28.814772", "87.627316,28.100825"],  # 从高德地图获取的坐标
        "estimated_distance": 1050,  # 根据高德地图实际数据更新
        "estimated_time": 15.75,  # 根据高德地图实际数据更新（15小时45分钟）
        "activities": "佩枯措和阿玛直米雪山观景",
        "accommodation": "日喀则市",
        "risk": "往返行程距离超长，实际约1050公里，15.75小时"
    },
    {
        "day": 8,
        "date": "2024-12-29",
        "weekday": "周日",
        "route": "日喀则 → 扎什伦布寺 → 当雄",
        "origin": "日喀则市",
        "destination": "当雄县",
        "waypoints": ["扎什伦布寺"],
        "estimated_distance": 400,
        "estimated_time": 6,
        "activities": "参观扎什伦布寺，前往纳木措区域",
        "accommodation": "当雄县"
    },
    {
        "day": 9,
        "date": "2024-12-30",
        "weekday": "周一",
        "route": "当雄 → 纳木措 → 拉萨 → 林芝机场",
        "origin": "当雄县",
        "destination": "林芝米林机场",
        "waypoints": ["纳木措", "拉萨市"],
        "estimated_distance": 740,
        "estimated_time": 11,
        "activities": "纳木措游览，返程送机",
        "accommodation": "行程结束",
        "risk": "车程极长，存在误机风险"
    }
]


def get_location_coordinate(location_name):
    """
    通过地点名称获取坐标
    
    Args:
        location_name: 地点名称
    
    Returns:
        str: 坐标字符串 "经度,纬度" 或 None
    """
    try:
        params = {
            "key": AMAP_API_KEY,
            "address": location_name,
            "city": "西藏"  # 限定在西藏自治区
        }
        
        response = requests.get(AMAP_GEOCODE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") == "1" and data.get("geocodes"):
            geocode = data["geocodes"][0]
            location = geocode.get("location")
            if location:
                return location
        
        return None
    except Exception as e:
        return None


def get_driving_route(origin, destination, waypoints=None):
    """
    调用高德地图API获取驾车路线信息
    
    Args:
        origin: 起点（地点名称或坐标）
        destination: 终点（地点名称或坐标）
        waypoints: 途经点列表（可选）
    
    Returns:
        dict: 包含距离（公里）和时间（分钟）的字典
    """
    if AMAP_API_KEY == "YOUR_API_KEY_HERE":
        print(f"⚠️  警告: 未配置高德地图API Key，使用估算值")
        return None
    
    try:
        # 尝试获取起点坐标
        origin_coord = get_location_coordinate(origin)
        if not origin_coord:
            origin_coord = origin  # 如果获取失败，使用原始值
        
        # 尝试获取终点坐标
        dest_coord = get_location_coordinate(destination)
        if not dest_coord:
            dest_coord = destination  # 如果获取失败，使用原始值
        
        # 构建请求参数
        params = {
            "key": AMAP_API_KEY,
            "origin": origin_coord,
            "destination": dest_coord,
            "extensions": "all",
            "strategy": "0"  # 0:速度优先（时间最短）
        }
        
        # 如果有途经点，获取坐标并添加到参数中
        if waypoints:
            waypoint_coords = []
            for wp in waypoints:
                wp_coord = get_location_coordinate(wp)
                if wp_coord:
                    waypoint_coords.append(wp_coord)
                else:
                    waypoint_coords.append(wp)  # 如果获取失败，使用原始值
            
            if waypoint_coords:
                waypoint_str = "|".join(waypoint_coords)
                params["waypoints"] = waypoint_str
        
        # 发送请求
        response = requests.get(AMAP_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") == "1" and data.get("route"):
            route = data["route"]
            paths = route.get("paths", [])
            
            if paths:
                path = paths[0]  # 取第一条路径
                distance = float(path.get("distance", 0)) / 1000  # 转换为公里
                duration = float(path.get("duration", 0)) / 60  # 转换为分钟
                
                return {
                    "distance_km": round(distance, 1),
                    "duration_minutes": round(duration, 1),
                    "duration_hours": round(duration / 60, 1)
                }
        else:
            error_info = data.get('info', '未知错误')
            if error_info != "INVALID_PARAMS":  # 不显示参数错误，因为可能是地点名称问题
                print(f"⚠️  API返回错误: {error_info}")
            return None
            
    except Exception as e:
        print(f"⚠️  调用API时出错: {str(e)}")
        return None


def analyze_itinerary():
    """
    分析整个行程，计算实际行车时间
    """
    results = []
    
    print("=" * 80)
    print("开始分析行程，正在调用高德地图API计算实际行车时间...")
    print("=" * 80)
    print()
    
    for item in ITINERARY:
        print(f"Day {item['day']} ({item['date']} {item['weekday']}): {item['route']}")
        
        # 调用API获取实际数据
        waypoints = item.get("waypoints")
        
        # 特殊处理：如果起点和终点相同（往返行程），计算往返距离
        if item["origin"] == item["destination"] and waypoints:
            # 如果有预定义的坐标，直接使用坐标进行路径规划
            if "waypoint_coords" in item and item["waypoint_coords"]:
                # 使用坐标进行路径规划
                origin_coord = get_location_coordinate(item["origin"])
                if not origin_coord:
                    origin_coord = item["origin"]
                
                # 构建完整的往返路径：起点 -> 途经点1 -> 途经点2 -> 起点
                waypoint_coords = item["waypoint_coords"]
                # 去程：起点 -> 途经点1 -> 途经点2
                api_result_go = get_driving_route(origin_coord, waypoint_coords[-1], waypoint_coords[:-1] if len(waypoint_coords) > 1 else None)
                # 返程：途经点2 -> 起点
                api_result_back = get_driving_route(waypoint_coords[-1], origin_coord)
                
                if api_result_go and api_result_back:
                    actual_distance = api_result_go["distance_km"] + api_result_back["distance_km"]
                    actual_duration_hours = api_result_go["duration_hours"] + api_result_back["duration_hours"]
                    actual_duration_minutes = api_result_go["duration_minutes"] + api_result_back["duration_minutes"]
                    api_result = {
                        "distance_km": actual_distance,
                        "duration_hours": actual_duration_hours,
                        "duration_minutes": actual_duration_minutes
                    }
                else:
                    # 如果API调用失败，使用从高德地图获取的实际数据
                    api_result = {
                        "distance_km": item.get("estimated_distance", 500),
                        "duration_hours": item.get("estimated_time", 8),
                        "duration_minutes": item.get("estimated_time", 8) * 60
                    }
            else:
                # 计算去程：起点到最远的途经点
                api_result_go = get_driving_route(item["origin"], waypoints[-1], waypoints[:-1] if len(waypoints) > 1 else None)
                # 计算返程：最远的途经点回到起点
                api_result_back = get_driving_route(waypoints[-1], item["origin"])
                
                if api_result_go and api_result_back:
                    actual_distance = api_result_go["distance_km"] + api_result_back["distance_km"]
                    actual_duration_hours = api_result_go["duration_hours"] + api_result_back["duration_hours"]
                    actual_duration_minutes = api_result_go["duration_minutes"] + api_result_back["duration_minutes"]
                    api_result = {
                        "distance_km": actual_distance,
                        "duration_hours": actual_duration_hours,
                        "duration_minutes": actual_duration_minutes
                    }
                else:
                    api_result = None
        else:
            api_result = get_driving_route(item["origin"], item["destination"], waypoints)
        
        if api_result:
            actual_distance = api_result["distance_km"]
            actual_duration_hours = api_result["duration_hours"]
            actual_duration_minutes = api_result["duration_minutes"]
            
            # 如果API返回的距离明显小于估算值（小于估算值的20%），可能是地点名称不准确
            # 对于这种情况，使用估算值
            if actual_distance > 0 and actual_distance < item["estimated_distance"] * 0.2:
                print(f"  ⚠️  注意: API返回距离({actual_distance}km)明显小于估算值，可能地点名称不准确")
                print(f"  ⚠️  使用估算值: {item['estimated_distance']} km, {item['estimated_time']} 小时")
                actual_distance = item["estimated_distance"]
                actual_duration_hours = item["estimated_time"]
                actual_duration_minutes = item["estimated_time"] * 60
        else:
            # 如果API调用失败，使用估算值
            actual_distance = item["estimated_distance"]
            actual_duration_hours = item["estimated_time"]
            actual_duration_minutes = item["estimated_time"] * 60
        
        # 计算差异
        distance_diff = actual_distance - item["estimated_distance"]
        time_diff = actual_duration_hours - item["estimated_time"]
        
        result = {
            "日期": item["date"],
            "星期": item["weekday"],
            "行程": item["route"],
            "起点": item["origin"],
            "终点": item["destination"],
            "估算距离(km)": item["estimated_distance"],
            "实际距离(km)": actual_distance,
            "距离差异(km)": round(distance_diff, 1),
            "估算时间(小时)": item["estimated_time"],
            "实际时间(小时)": actual_duration_hours,
            "实际时间(分钟)": actual_duration_minutes,
            "时间差异(小时)": round(time_diff, 1),
            "活动安排": item["activities"],
            "住宿": item["accommodation"],
            "风险提示": item.get("risk", "")
        }
        
        results.append(result)
        
        # 打印结果
        if api_result:
            print(f"  ✓ 实际距离: {actual_distance} km")
            print(f"  ✓ 实际时间: {actual_duration_hours} 小时 ({actual_duration_minutes} 分钟)")
        else:
            print(f"  ⚠ 使用估算值: {actual_distance} km, {actual_duration_hours} 小时")
        
        if distance_diff != 0 or time_diff != 0:
            print(f"  📊 差异: 距离 {distance_diff:+.1f} km, 时间 {time_diff:+.1f} 小时")
        
        if item.get("risk"):
            print(f"  ⚠️  风险: {item['risk']}")
        
        print()
        
        # 避免API调用过于频繁
        time.sleep(0.5)
    
    return results


def generate_report(results):
    """
    生成Excel报表
    """
    df = pd.DataFrame(results)
    
    # 生成Excel文件
    excel_file = "西藏行程分析报告.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # 详细报表
        df.to_excel(writer, sheet_name='详细行程', index=False)
        
        # 汇总统计
        summary_data = {
            "统计项": [
                "总天数",
                "总估算距离(km)",
                "总实际距离(km)",
                "总估算时间(小时)",
                "总实际时间(小时)",
                "平均每日距离(km)",
                "平均每日时间(小时)",
                "最长单日距离(km)",
                "最长单日时间(小时)",
                "最短单日距离(km)",
                "最短单日时间(小时)"
            ],
            "数值": [
                len(results),
                sum(r["估算距离(km)"] for r in results),
                sum(r["实际距离(km)"] for r in results),
                sum(r["估算时间(小时)"] for r in results),
                sum(r["实际时间(小时)"] for r in results),
                round(sum(r["实际距离(km)"] for r in results) / len(results), 1),
                round(sum(r["实际时间(小时)"] for r in results) / len(results), 1),
                max(r["实际距离(km)"] for r in results),
                max(r["实际时间(小时)"] for r in results),
                min(r["实际距离(km)"] for r in results),
                min(r["实际时间(小时)"] for r in results)
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='汇总统计', index=False)
        
        # 风险分析
        risk_items = [r for r in results if r["风险提示"]]
        if risk_items:
            risk_df = pd.DataFrame([
                {
                    "日期": r["日期"],
                    "行程": r["行程"],
                    "实际时间(小时)": r["实际时间(小时)"],
                    "风险提示": r["风险提示"]
                }
                for r in risk_items
            ])
            risk_df.to_excel(writer, sheet_name='风险分析', index=False)
    
    print(f"✓ 报表已生成: {excel_file}")
    return excel_file


def feasibility_analysis(results):
    """
    分析行程可行性
    """
    print("=" * 80)
    print("行程可行性分析")
    print("=" * 80)
    print()
    
    total_distance = sum(r["实际距离(km)"] for r in results)
    total_time = sum(r["实际时间(小时)"] for r in results)
    avg_distance = total_distance / len(results)
    avg_time = total_time / len(results)
    max_time = max(r["实际时间(小时)"] for r in results)
    max_distance = max(r["实际距离(km)"] for r in results)
    
    print(f"📊 总体数据:")
    print(f"  总行程距离: {total_distance:.1f} 公里")
    print(f"  总行车时间: {total_time:.1f} 小时 ({total_time/24:.1f} 天)")
    print(f"  平均每日距离: {avg_distance:.1f} 公里")
    print(f"  平均每日时间: {avg_time:.1f} 小时")
    print()
    
    print(f"⚠️  关键风险点:")
    
    # 分析高风险日
    high_risk_days = []
    for r in results:
        if r["实际时间(小时)"] >= 8:
            high_risk_days.append(r)
        if r["风险提示"]:
            print(f"  • Day {results.index(r)+1} ({r['日期']}): {r['风险提示']}")
            print(f"    实际时间: {r['实际时间(小时)']} 小时")
    
    if high_risk_days:
        print()
        print(f"  • 超过8小时的长途驾驶日: {len(high_risk_days)} 天")
        for day in high_risk_days:
            print(f"    - Day {results.index(day)+1}: {day['实际时间(小时)']} 小时 ({day['行程']})")
    
    print()
    print(f"💡 可行性评估:")
    
    # 评估标准
    issues = []
    recommendations = []
    
    if max_time >= 10:
        issues.append(f"最长单日行程达到 {max_time:.1f} 小时，存在严重疲劳驾驶风险")
        recommendations.append("建议拆分最长行程或增加休息日")
    
    if total_time / len(results) >= 7:
        issues.append(f"平均每日行车时间 {avg_time:.1f} 小时，强度较高")
        recommendations.append("建议适当减少每日行程，增加缓冲时间")
    
    if len([r for r in results if r["实际时间(小时)"] >= 8]) >= 3:
        issues.append("超过3天行程超过8小时，整体强度过大")
        recommendations.append("建议优化路线，减少长途驾驶天数")
    
    # 检查最后一天
    last_day = results[-1]
    if last_day["实际时间(小时)"] >= 10:
        issues.append(f"最后一天行程 {last_day['实际时间(小时)']} 小时，存在误机风险")
        recommendations.append("强烈建议将返程航班延后一天，或提前一天结束行程")
    
    if issues:
        print("  ❌ 存在的问题:")
        for issue in issues:
            print(f"    • {issue}")
        print()
        print("  ✅ 建议措施:")
        for rec in recommendations:
            print(f"    • {rec}")
    else:
        print("  ✅ 行程整体可行，但需注意:")
        print("    • 冬季路况可能影响实际行驶时间")
        print("    • 高海拔地区需要适应时间")
        print("    • 建议预留20-30%的缓冲时间")
    
    print()
    print("=" * 80)


def main():
    """
    主函数
    """
    print("\n")
    print("🚗 西藏行程分析工具")
    print("=" * 80)
    print()
    
    if AMAP_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  注意: 未配置高德地图API Key")
        print("   请在 config.py 中设置 AMAP_API_KEY")
        print("   当前将使用行程表中的估算值进行分析")
        print()
        input("按回车键继续...")
        print()
    
    # 分析行程
    results = analyze_itinerary()
    
    # 生成报表
    excel_file = generate_report(results)
    
    # 可行性分析
    feasibility_analysis(results)
    
    print(f"\n✅ 分析完成！详细报表已保存至: {excel_file}\n")


if __name__ == "__main__":
    main()

