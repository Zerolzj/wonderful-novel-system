#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网文平台自动发布系统
支持多平台章节自动发布、审核状态监控、数据统计
"""

import requests
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class PlatformType(Enum):
    QIDIAN = "qidian"      # 起点中文网
    FEILU = "feilu"        # 飞卢小说网
    SHIQI = "17k"          # 17K小说网

@dataclass
class ChapterData:
    """章节数据结构"""
    title: str
    content: str
    chapter_number: int
    word_count: int
    tags: List[str] = None
    category: str = "玄幻"

class SensitiveWordFilter:
    """敏感词过滤器"""
    
    def __init__(self):
        # 敏感词列表（示例）
        self.sensitive_words = [
            "政治", "暴力", "色情", "赌博", "毒品",
            "恐怖", "极端", "分裂", "颠覆", "造谣"
        ]
    
    def filter_content(self, content: str) -> str:
        """过滤敏感词"""
        for word in self.sensitive_words:
            content = content.replace(word, "***")
        return content

class ContentPreprocessor:
    """内容预处理器"""
    
    def __init__(self):
        self.filter = SensitiveWordFilter()
    
    def preprocess(self, chapter: ChapterData) -> ChapterData:
        """预处理章节内容"""
        # 过滤敏感词
        chapter.content = self.filter.filter_content(chapter.content)
        
        # 清理格式
        chapter.content = self._clean_format(chapter.content)
        
        # 统计字数
        chapter.word_count = len(chapter.content)
        
        return chapter
    
    def _clean_format(self, content: str) -> str:
        """清理格式"""
        # 移除多余的空行
        content = '\n'.join(line for line in content.split('\n') if line.strip())
        
        # 确保段落间有适当的空行
        paragraphs = content.split('\n\n')
        cleaned_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                cleaned_paragraphs.append(para.strip())
        
        return '\n\n'.join(cleaned_paragraphs)

class QidianPublisher:
    """起点中文网发布器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.base_url = "https://api.qidian.com"
        self.headers = {
            "Authorization": f"Bearer {config['token']}",
            "Content-Type": "application/json"
        }
    
    def publish_chapter(self, chapter: ChapterData) -> Dict:
        """发布章节"""
        url = f"{self.base_url}/chapters"
        
        data = {
            "book_id": self.config["book_id"],
            "title": chapter.title,
            "content": chapter.content,
            "chapter_number": chapter.chapter_number,
            "word_count": chapter.word_count
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def check_status(self, chapter_id: str) -> Dict:
        """检查审核状态"""
        url = f"{self.base_url}/chapters/{chapter_id}/status"
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class FeiluPublisher:
    """飞卢小说网发布器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.base_url = "https://api.feilu.com"
        self.headers = {
            "Authorization": f"Bearer {config['token']}",
            "Content-Type": "application/json"
        }
    
    def publish_chapter(self, chapter: ChapterData) -> Dict:
        """发布章节（支持批量）"""
        url = f"{self.base_url}/chapters/batch"
        
        data = {
            "book_id": self.config["book_id"],
            "chapters": [{
                "title": chapter.title,
                "content": chapter.content,
                "chapter_number": chapter.chapter_number
            }]
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def check_status(self, chapter_id: str) -> Dict:
        """检查审核状态"""
        url = f"{self.base_url}/chapters/{chapter_id}/status"
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class ShiqiPublisher:
    """17K小说网发布器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.base_url = "https://api.17k.com"
        self.headers = {
            "Authorization": f"Bearer {config['token']}",
            "Content-Type": "application/json"
        }
    
    def publish_chapter(self, chapter: ChapterData) -> Dict:
        """发布章节（支持Markdown）"""
        url = f"{self.base_url}/chapters"
        
        data = {
            "book_id": self.config["book_id"],
            "title": chapter.title,
            "content": chapter.content,  # 支持Markdown
            "format": "markdown",
            "chapter_number": chapter.chapter_number
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def check_status(self, chapter_id: str) -> Dict:
        """检查审核状态"""
        url = f"{self.base_url}/chapters/{chapter_id}/status"
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class PlatformPublisher:
    """平台发布管理器"""
    
    def __init__(self, config_file: str = "platform_config.json"):
        self.config = self._load_config(config_file)
        self.preprocessor = ContentPreprocessor()
        self.publishers = self._init_publishers()
    
    def _load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_config(config_file)
    
    def _create_default_config(self, config_file: str) -> Dict:
        """创建默认配置"""
        default_config = {
            "platforms": {
                "qidian": {
                    "enabled": False,
                    "token": "",
                    "book_id": ""
                },
                "feilu": {
                    "enabled": False,
                    "token": "",
                    "book_id": ""
                },
                "17k": {
                    "enabled": False,
                    "token": "",
                    "book_id": ""
                }
            }
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        return default_config
    
    def _init_publishers(self) -> Dict:
        """初始化发布器"""
        publishers = {}
        
        if self.config["platforms"]["qidian"]["enabled"]:
            publishers["qidian"] = QidianPublisher(self.config["platforms"]["qidian"])
        
        if self.config["platforms"]["feilu"]["enabled"]:
            publishers["feilu"] = FeiluPublisher(self.config["platforms"]["feilu"])
        
        if self.config["platforms"]["17k"]["enabled"]:
            publishers["17k"] = ShiqiPublisher(self.config["platforms"]["17k"])
        
        return publishers
    
    def publish_chapter(self, chapter: ChapterData, platforms: List[str] = None) -> Dict:
        """发布章节到指定平台"""
        if platforms is None:
            platforms = list(self.publishers.keys())
        
        # 预处理内容
        chapter = self.preprocessor.preprocess(chapter)
        
        results = {}
        
        for platform in platforms:
            if platform in self.publishers:
                try:
                    result = self.publishers[platform].publish_chapter(chapter)
                    results[platform] = result
                    
                    # 记录发布状态
                    self._log_publish_result(platform, chapter, result)
                    
                except Exception as e:
                    results[platform] = {"error": str(e)}
        
        return results
    
    def check_all_status(self) -> Dict:
        """检查所有平台的审核状态"""
        status_results = {}
        
        for platform, publisher in self.publishers.items():
            try:
                # 这里需要从数据库或文件中获取章节ID列表
                # 暂时返回空状态
                status_results[platform] = {"status": "checked"}
            except Exception as e:
                status_results[platform] = {"error": str(e)}
        
        return status_results
    
    def _log_publish_result(self, platform: str, chapter: ChapterData, result: Dict):
        """记录发布结果"""
        log_entry = {
            "timestamp": time.time(),
            "platform": platform,
            "chapter": chapter.chapter_number,
            "title": chapter.title,
            "result": result
        }
        
        # 这里可以记录到数据库或文件
        print(f"Published to {platform}: {chapter.title} - {result}")

def main():
    """主函数 - 示例用法"""
    # 创建发布管理器
    publisher = PlatformPublisher()
    
    # 创建章节示例
    chapter = ChapterData(
        title="第一章：系统觉醒",
        content="这是第一章的内容...",
        chapter_number=1,
        word_count=3500,
        tags=["系统", "穿越", "玄幻"],
        category="玄幻"
    )
    
    # 发布到所有启用的平台
    results = publisher.publish_chapter(chapter)
    
    print("发布结果:")
    for platform, result in results.items():
        print(f"{platform}: {result}")

if __name__ == "__main__":
    main()