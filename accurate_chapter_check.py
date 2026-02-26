#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from datetime import datetime

def count_chinese_chars(text):
    """统计中文字数（不包括标点符号）"""
    # 移除代码块
    text = re.sub(r'```[\s\S]*?```', '', text)
    # 移除markdown标记
    text = re.sub(r'[#*`\[\]()_-]', '', text)
    # 统计中文字符（不包括标点符号）
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', text)
    return len(chinese_chars)

def count_elements(text, patterns):
    """统计特定元素出现次数"""
    count = 0
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        count += len(matches)
    return count

def check_chapter_quality(file_path):
    """检查单个章节质量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chapter_name = os.path.basename(file_path).replace('.md', '')
        
        # 统计字数
        word_count = count_chinese_chars(content)
        
        # 定义关键词模式
        code_patterns = [
            r'代码|系统|函数|算法|编程|数据|逻辑|循环|条件|变量|数组|对象|类|方法|接口|API|JSON|HTML|CSS|JavaScript|Python|Java|C\+\+|SQL|数据库|框架|库|包|模块|调试|测试|优化|重构|部署|版本控制'
        ]
        
        cultivation_patterns = [
            r'修仙|灵气|功法|境界|突破|炼丹|炼器|阵法|符箓|丹药|灵石|法宝|洞府|宗门|师父|师兄|师姐|师弟|师妹|长老|宗主|天劫|飞升|仙界|人间|魔界|妖界|神界|道心|悟道|修行|修炼|真元|元神|金丹|元婴|化神|返虚|合体|大乘|渡劫'
        ]
        
        growth_patterns = [
            r'成长|进步|提升|突破|领悟|学会|掌握|熟练|精通|创新|改进|完善|升级|进化|蜕变|飞跃|超越|战胜|击败|克服|解决|应对|适应|改变'
        ]
        
        exciting_patterns = [
            r'震撼|惊人|不可思议|难以置信|令人惊叹|震撼人心|惊心动魄|热血沸腾|激动人心|痛快|爽快|过瘾|解气|扬眉吐气|一鸣惊人|大放异彩|脱颖而出|技惊四座|震惊全场|全场沸腾|掌声雷动|欢呼声|赞叹声'
        ]
        
        # 统计各元素数量
        code_count = count_elements(content, code_patterns)
        cultivation_count = count_elements(content, cultivation_patterns)
        growth_count = count_elements(content, growth_patterns)
        exciting_count = count_elements(content, exciting_patterns)
        
        # 质量判断
        is_qualified = True
        issues = []
        
        # 字数检查
        if word_count < 3000:
            is_qualified = False
            issues.append(f"字数不足({word_count}字)")
        elif word_count > 4000:
            is_qualified = False
            issues.append(f"字数过多({word_count}字)")
        
        # 元素检查
        if code_count < 5:
            is_qualified = False
            issues.append(f"代码元素不足({code_count}处)")
        
        if cultivation_count < 5:
            is_qualified = False
            issues.append(f"修仙元素不足({cultivation_count}处)")
        
        if growth_count < 3:
            is_qualified = False
            issues.append(f"成长元素不足({growth_count}处)")
        
        if exciting_count < 2:
            is_qualified = False
            issues.append(f"爽点不足({exciting_count}处)")
        
        return {
            'chapter': chapter_name,
            'word_count': word_count,
            'code_count': code_count,
            'cultivation_count': cultivation_count,
            'growth_count': growth_count,
            'exciting_count': exciting_count,
            'is_qualified': is_qualified,
            'issues': issues
        }
    
    except Exception as e:
        return {
            'chapter': os.path.basename(file_path).replace('.md', ''),
            'error': str(e)
        }

def main():
    """主函数"""
    base_path = "/Users/zero/.openclaw/workspace/万界神级系统"
    
    # 获取所有章节文件
    chapters = []
    for file in os.listdir(base_path):
        if file.startswith("第") and file.endswith(".md"):
            if "创作中" not in file and "反馈" not in file and "进度" not in file:
                chapters.append(os.path.join(base_path, file))
    
    chapters.sort()  # 按文件名排序
    
    print("开始章节质量检查...")
    print("=" * 60)
    
    results = []
    qualified_count = 0
    
    for chapter_file in chapters:
        result = check_chapter_quality(chapter_file)
        results.append(result)
        
        if 'error' in result:
            print(f"❌ {result['chapter']} - 检查出错: {result['error']}")
        else:
            if result['is_qualified']:
                print(f"✅ {result['chapter']} - 合格 ({result['word_count']}字)")
                qualified_count += 1
            else:
                issues_str = "; ".join(result['issues'])
                print(f"❌ {result['chapter']} - 不合格: {issues_str}")
    
    print("=" * 60)
    print("检查完成！")
    print(f"总章节数: {len(chapters)}")
    print(f"合格章节: {qualified_count}")
    print(f"合格率: {qualified_count * 100 // len(chapters)}%")
    
    # 生成详细报告
    report = {
        'check_time': datetime.now().isoformat(),
        'total_chapters': len(chapters),
        'qualified_chapters': qualified_count,
        'qualification_rate': qualified_count * 100 // len(chapters),
        'results': results
    }
    
    # 保存报告
    report_path = "/Users/zero/.openclaw/workspace/chapter_quality_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细报告已保存至: {report_path}")
    
    # 更新日志
    log_entry = f"\n{datetime.now()}: 章节质量检查完成 - 总计{len(chapters)}章，合格{qualified_count}章，合格率{qualified_count * 100 // len(chapters)}%\n"
    with open("/Users/zero/.openclaw/workspace/memory/2026-02-26.md", 'a', encoding='utf-8') as f:
        f.write(log_entry)

if __name__ == "__main__":
    main()