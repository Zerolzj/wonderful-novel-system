#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《万界神级系统》读者反馈监控执行脚本
专门监控第31-40章的读者反馈，分析评论质量，提供改进建议
"""

import json
import time
import datetime
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class SentimentType(Enum):
    """情感分析类型"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class FeedbackCategory(Enum):
    """反馈分类"""
    PLOT = "plot"           # 剧情相关
    SETTING = "setting"     # 设定相关
    CHARACTER = "character" # 人物相关
    TECHNICAL = "technical" # 技术元素
    PACING = "pacing"       # 节奏相关
    WRITING = "writing"     # 写作质量

@dataclass
class FeedbackEntry:
    """反馈条目"""
    id: str
    content: str
    author: str
    timestamp: datetime.datetime
    platform: str
    chapter: int
    sentiment: SentimentType
    category: FeedbackCategory
    keywords: List[str]
    likes: int = 0
    replies: int = 0

class ReaderFeedbackMonitor:
    """读者反馈监控器"""
    
    def __init__(self, start_chapter: int = 31, end_chapter: int = 40):
        self.start_chapter = start_chapter
        self.end_chapter = end_chapter
        self.feedback_data: List[FeedbackEntry] = []
        self.keywords_map = {
            FeedbackCategory.PLOT: ["剧情", "故事", "情节", "发展", "转折", "高潮"],
            FeedbackCategory.SETTING: ["设定", "世界观", "新世界", "魔法编程", "代码修仙", "系统"],
            FeedbackCategory.CHARACTER: ["林辰", "苏晴雨", "陈浩", "角色", "人物", "性格"],
            FeedbackCategory.TECHNICAL: ["代码", "编程", "技术", "cast", "函数", "算法"],
            FeedbackCategory.PACING: ["节奏", "速度", "拖沓", "紧凑", "发展", "推进"],
            FeedbackCategory.WRITING: ["文笔", "写法", "表达", "描写", "语句", "修辞"]
        }
        self.sentiment_keywords = {
            SentimentType.POSITIVE: ["好", "棒", "赞", "喜欢", "期待", "精彩", "新颖", "有趣"],
            SentimentType.NEGATIVE: ["差", "烂", "讨厌", "失望", "无聊", "老套", "问题", "错误"],
            SentimentType.NEUTRAL: ["还行", "一般", "普通", "正常", "可以", "不错"]
        }
    
    def analyze_sentiment(self, text: str) -> SentimentType:
        """情感分析"""
        positive_count = sum(1 for word in self.sentiment_keywords[SentimentType.POSITIVE] if word in text)
        negative_count = sum(1 for word in self.sentiment_keywords[SentimentType.NEGATIVE] if word in text)
        
        if positive_count > negative_count:
            return SentimentType.POSITIVE
        elif negative_count > positive_count:
            return SentimentType.NEGATIVE
        else:
            return SentimentType.NEUTRAL
    
    def categorize_feedback(self, text: str) -> FeedbackCategory:
        """反馈分类"""
        category_scores = {}
        for category, keywords in self.keywords_map.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
        
        if max(category_scores.values()) == 0:
            return FeedbackCategory.PLOT  # 默认分类
        
        return max(category_scores, key=category_scores.get)
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        all_keywords = []
        for keywords in self.keywords_map.values():
            all_keywords.extend(keywords)
        
        found_keywords = [keyword for keyword in all_keywords if keyword in text]
        return found_keywords
    
    def add_feedback(self, content: str, author: str, platform: str, 
                    chapter: int, likes: int = 0, replies: int = 0) -> FeedbackEntry:
        """添加反馈条目"""
        feedback_id = f"{platform}_{int(time.time())}_{len(self.feedback_data)}"
        
        sentiment = self.analyze_sentiment(content)
        category = self.categorize_feedback(content)
        keywords = self.extract_keywords(content)
        
        entry = FeedbackEntry(
            id=feedback_id,
            content=content,
            author=author,
            timestamp=datetime.datetime.now(),
            platform=platform,
            chapter=chapter,
            sentiment=sentiment,
            category=category,
            keywords=keywords,
            likes=likes,
            replies=replies
        )
        
        self.feedback_data.append(entry)
        return entry
    
    def generate_chapter_report(self, chapter: int) -> Dict[str, Any]:
        """生成章节报告"""
        chapter_feedback = [f for f in self.feedback_data if f.chapter == chapter]
        
        if not chapter_feedback:
            return {"error": f"第{chapter}章暂无反馈数据"}
        
        total_feedback = len(chapter_feedback)
        positive_count = sum(1 for f in chapter_feedback if f.sentiment == SentimentType.POSITIVE)
        negative_count = sum(1 for f in chapter_feedback if f.sentiment == SentimentType.NEGATIVE)
        neutral_count = sum(1 for f in chapter_feedback if f.sentiment == SentimentType.NEUTRAL)
        
        category_distribution = {}
        for category in FeedbackCategory:
            category_count = sum(1 for f in chapter_feedback if f.category == category)
            category_distribution[category.value] = {
                "count": category_count,
                "percentage": round(category_count / total_feedback * 100, 2)
            }
        
        # 提取热门关键词
        all_keywords = []
        for f in chapter_feedback:
            all_keywords.extend(f.keywords)
        
        keyword_frequency = {}
        for keyword in all_keywords:
            keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        top_keywords = sorted(keyword_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 计算参与度指标
        total_likes = sum(f.likes for f in chapter_feedback)
        total_replies = sum(f.replies for f in chapter_feedback)
        avg_likes = total_likes / total_feedback if total_feedback > 0 else 0
        avg_replies = total_replies / total_feedback if total_feedback > 0 else 0
        
        return {
            "chapter": chapter,
            "total_feedback": total_feedback,
            "sentiment_analysis": {
                "positive": {
                    "count": positive_count,
                    "percentage": round(positive_count / total_feedback * 100, 2)
                },
                "negative": {
                    "count": negative_count,
                    "percentage": round(negative_count / total_feedback * 100, 2)
                },
                "neutral": {
                    "count": neutral_count,
                    "percentage": round(neutral_count / total_feedback * 100, 2)
                }
            },
            "category_distribution": category_distribution,
            "top_keywords": top_keywords,
            "engagement_metrics": {
                "total_likes": total_likes,
                "total_replies": total_replies,
                "average_likes": round(avg_likes, 2),
                "average_replies": round(avg_replies, 2)
            },
            "report_time": datetime.datetime.now().isoformat()
        }
    
    def generate_improvement_suggestions(self, chapter: int) -> List[str]:
        """生成改进建议"""
        chapter_feedback = [f for f in self.feedback_data if f.chapter == chapter]
        
        if not chapter_feedback:
            return ["暂无足够数据生成建议"]
        
        suggestions = []
        negative_feedback = [f for f in chapter_feedback if f.sentiment == SentimentType.NEGATIVE]
        
        # 分析负面反馈的主要问题
        category_issues = {}
        for feedback in negative_feedback:
            if feedback.category not in category_issues:
                category_issues[feedback.category] = []
            category_issues[feedback.category].append(feedback.content)
        
        for category, issues in category_issues.items():
            if len(issues) >= 3:  # 如果某类问题超过3条
                if category == FeedbackCategory.PLOT:
                    suggestions.append("剧情方面需要加强逻辑性和连贯性，建议重新梳理故事线")
                elif category == FeedbackCategory.SETTING:
                    suggestions.append("世界观设定需要更详细的解释和铺垫，避免读者困惑")
                elif category == FeedbackCategory.CHARACTER:
                    suggestions.append("人物塑造需要更加立体，增加角色深度和成长弧线")
                elif category == FeedbackCategory.TECHNICAL:
                    suggestions.append("技术元素需要更准确的表达，确保代码示例的正确性")
                elif category == FeedbackCategory.PACING:
                    suggestions.append("剧情节奏需要调整，避免过快或过慢的问题")
                elif category == FeedbackCategory.WRITING:
                    suggestions.append("写作技巧需要提升，加强语言表达和描写能力")
        
        # 分析整体情感倾向
        total_negative = len(negative_feedback)
        total_feedback = len(chapter_feedback)
        negative_rate = total_negative / total_feedback if total_feedback > 0 else 0
        
        if negative_rate > 0.3:
            suggestions.append("负面反馈比例较高，建议全面审视章节内容，考虑重大调整")
        elif negative_rate > 0.2:
            suggestions.append("负面反馈比例中等，建议针对性改进主要问题")
        
        if not suggestions:
            suggestions.append("整体反馈良好，继续保持当前创作方向")
        
        return suggestions
    
    def save_report(self, chapter: int, filename: str = None) -> str:
        """保存报告到文件"""
        if filename is None:
            filename = f"第{chapter}章反馈报告_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = self.generate_chapter_report(chapter)
        suggestions = self.generate_improvement_suggestions(chapter)
        
        full_report = {
            "report": report,
            "suggestions": suggestions,
            "feedback_entries": [
                {
                    "id": f.id,
                    "content": f.content,
                    "author": f.author,
                    "platform": f.platform,
                    "sentiment": f.sentiment.value,
                    "category": f.category.value,
                    "keywords": f.keywords,
                    "likes": f.likes,
                    "replies": f.replies,
                    "timestamp": f.timestamp.isoformat()
                }
                for f in self.feedback_data if f.chapter == chapter
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """主函数 - 演示监控器使用"""
    monitor = ReaderFeedbackMonitor(31, 40)
    
    # 模拟添加一些反馈数据
    sample_feedbacks = [
        ("第31章的新世界设定很有意思，魔法编程的概念很新颖！", "程序员小王", "起点中文网", 31, 15, 3),
        ("cast fireball()的例子太形象了，瞬间就理解了魔法编程的概念", "代码修仙爱好者", "纵横中文网", 31, 12, 2),
        ("七个世界的设定有点多，担心后面会记不住", "谨慎读者", "17K小说网", 31, 5, 8),
        ("传送的逻辑有点问题，能量来源没说清楚", "逻辑控", "起点中文网", 31, 2, 5),
        ("终于等到新世界了！期待后续的发展", "忠实读者", "起点中文网", 31, 20, 4),
        ("林辰的程序员思维在新世界里应该会有很大优势", "技术宅", "知乎", 31, 8, 1),
        ("新角色艾德有点模板化，希望能有更多深度", "角色控", "贴吧", 31, 3, 6),
        ("代码修仙到魔法编程的转换很自然，逻辑通顺", "理性分析者", "起点中文网", 31, 18, 2)
    ]
    
    for content, author, platform, chapter, likes, replies in sample_feedbacks:
        monitor.add_feedback(content, author, platform, chapter, likes, replies)
    
    # 生成第31章报告
    report = monitor.generate_chapter_report(31)
    suggestions = monitor.generate_improvement_suggestions(31)
    
    print("=== 第31章读者反馈监控报告 ===")
    print(f"总反馈数: {report['total_feedback']}")
    print(f"正面反馈: {report['sentiment_analysis']['positive']['percentage']}%")
    print(f"负面反馈: {report['sentiment_analysis']['negative']['percentage']}%")
    print(f"中性反馈: {report['sentiment_analysis']['neutral']['percentage']}%")
    
    print("\n=== 主要反馈分类 ===")
    for category, data in report['category_distribution'].items():
        if data['count'] > 0:
            print(f"{category}: {data['count']}条 ({data['percentage']}%)")
    
    print("\n=== 热门关键词 ===")
    for keyword, count in report['top_keywords']:
        print(f"{keyword}: {count}次")
    
    print("\n=== 改进建议 ===")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    # 保存报告
    filename = monitor.save_report(31)
    print(f"\n报告已保存到: {filename}")

if __name__ == "__main__":
    main()