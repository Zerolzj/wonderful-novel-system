#!/bin/bash

echo "开始最终清理和标准化章节文件..."

cd "/Users/zero/.openclaw/workspace/万界神级系统/chapters/volume1"

# 1. 移动重复版本和临时文件到archive
echo "移动重复版本和临时文件..."

# 移动重制版文件
for file in *重制版.md; do
    if [ -f "$file" ]; then
        mv "$file" "../../archive/"
        echo "✅ 移动重制版: $file"
    fi
done

# 移动创作中文件
for file in *创作中.md; do
    if [ -f "$file" ]; then
        mv "$file" "../../archive/"
        echo "✅ 移动创作中: $file"
    fi
done

# 移动反馈分析和优化方案
for file in *反馈分析* *优化方案*.md; do
    if [ -f "$file" ]; then
        mv "$file" "../../docs/reports/"
        echo "✅ 移动反馈分析: $file"
    fi
done

# 移动异常命名的文件
for file in 万界神级系统第*.md; do
    if [ -f "$file" ]; then
        mv "$file" "../../archive/"
        echo "✅ 移动异常命名: $file"
    fi
done

# 移动双重.md后缀的文件
for file in *.md.md; do
    if [ -f "$file" ]; then
        # 重命名为正确的.md文件
        new_name=$(echo "$file" | sed 's/\.md\.md$/.md/')
        mv "$file" "$new_name"
        echo "✅ 修正双重后缀: $file -> $new_name"
    fi
done

# 2. 检查并整理标准章节文件
echo ""
echo "检查标准章节文件..."

# 统计标准章节
standard_count=$(ls | grep -E "^第[0-9]+章-" | wc -l)
echo "标准章节文件数量: $standard_count"

# 列出所有标准章节
echo "标准章节列表："
ls | grep -E "^第[0-9]+章-" | sort -V

# 3. 验证章节连续性
echo ""
echo "验证章节连续性..."

# 获取所有章节编号
chapters=$(ls | grep -E "^第[0-9]+章-" | sed 's/^第\([0-9]*\)章-.*/\1/' | sort -n)

missing_chapters=""
for i in {1..100}; do
    if ! echo "$chapters" | grep -q "^$i$"; then
        missing_chapters="$missing_chapters $i"
    fi
done

if [ -n "$missing_chapters" ]; then
    echo "⚠️  缺失章节:$missing_chapters"
else
    echo "✅ 所有1-100章都存在"
fi

# 4. 显示最终统计
echo ""
echo "=== 最终清理结果 ==="
echo "标准章节: $standard_count"
echo "volume1目录总文件数: $(ls | wc -l)"

echo ""
echo "✅ 文件整理完成！"