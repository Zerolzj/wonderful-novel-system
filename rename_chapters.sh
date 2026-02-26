#!/bin/bash

echo "开始文件重命名和清理..."

# 进入章节目录
cd 万界神级系统/chapters

# 处理volume1 - 第一卷 (1-25章)
echo "整理第一卷文件..."
for file in 万界神级系统_第*.md; do
    # 提取章节号
    chapter_num=$(echo "$file" | sed 's/万界神级系统_第\([0-9]*\)章.*/\1/')
    if [ -n "$chapter_num" ]; then
        # 获取标题
        title=$(echo "$file" | sed 's/万界神级系统_第[0-9]*章_\(.*\)\.md/\1/')
        # 重命名
        new_name="第${chapter_num}章-${title}.md"
        mv "$file" "volume1/$new_name"
        echo "重命名: $file -> volume1/$new_name"
    fi
done

# 移动第26-50章到volume2
echo "整理第二卷文件..."
for i in {26..50}; do
    file=$(ls 万界神级系统_第${i}章*.md 2>/dev/null)
    if [ -n "$file" ]; then
        title=$(echo "$file" | sed 's/万界神级系统_第[0-9]*章_\(.*\)\.md/\1/')
        new_name="第${i}章-${title}.md"
        mv "$file" "volume2/$new_name"
        echo "移动到第二卷: $file -> volume2/$new_name"
    fi
done

# 移动第51-75章到volume3
echo "整理第三卷文件..."
for i in {51..75}; do
    file=$(ls 万界神级系统_第${i}章*.md 2>/dev/null)
    if [ -n "$file" ]; then
        title=$(echo "$file" | sed 's/万界神级系统_第[0-9]*章_\(.*\)\.md/\1/')
        new_name="第${i}章-${title}.md"
        mv "$file" "volume3/$new_name"
        echo "移动到第三卷: $file -> volume3/$new_name"
    fi
done

# 移动第76-100章到volume4
echo "整理第四卷文件..."
for i in {76..100}; do
    file=$(ls 万界神级系统_第${i}章*.md 2>/dev/null)
    if [ -n "$file" ]; then
        title=$(echo "$file" | sed 's/万界神级系统_第[0-9]*章_\(.*\)\.md/\1/')
        new_name="第${i}章-${title}.md"
        mv "$file" "volume4/$new_name"
        echo "移动到第四卷: $file -> volume4/$new_name"
    fi
done

echo "文件重命名和清理完成！"