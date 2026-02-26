#!/bin/bash

echo "开始整理《万界神级系统》文件夹..."

# 创建新的文件夹结构
mkdir -p 万界神级系统/chapters/volume1
mkdir -p 万界神级系统/chapters/volume2  
mkdir -p 万界神级系统/chapters/volume3
mkdir -p 万界神级系统/chapters/volume4
mkdir -p 万界神级系统/docs/planning
mkdir -p 万界神级系统/docs/feedback
mkdir -p 万界神级系统/docs/reports
mkdir -p 万界神级系统/archive

echo "文件夹结构创建完成"

# 移动现有章节文件到新结构
echo "开始移动章节文件..."

# 第一卷 (1-25章)
mv 万界神级系统/第*.md 万界神级系统/chapters/volume1/ 2>/dev/null || true

# 移动根目录下的章节文件
find . -maxdepth 1 -name "万界神级系统_第*.md" -exec mv {} 万界神级系统/chapters/ \;

echo "章节文件移动完成"

# 移动文档文件
echo "开始整理文档文件..."
mv 万界神级系统/*反馈*.md 万界神级系统/docs/feedback/ 2>/dev/null || true
mv 万界神级系统/*报告*.md 万界神级系统/docs/reports/ 2>/dev/null || true
mv 万界神级系统/*分析*.md 万界神级系统/docs/feedback/ 2>/dev/null || true
mv 万界神级系统/*优化*.md 万界神级系统/docs/planning/ 2>/dev/null || true

echo "文档整理完成"

# 移动废弃文件到archive
echo "开始清理废弃文件..."
mv 万界神级系统*第*.txt 万界神级系统/archive/ 2>/dev/null || true
mv 万界神级系统*重制版.md 万界神级系统/archive/ 2>/dev/null || true

echo "废弃文件清理完成"

echo "整理完成！"