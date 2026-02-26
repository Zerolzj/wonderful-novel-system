#!/bin/bash

echo "开始彻底整理《万界神级系统》文件夹..."

# 进入工作目录
cd "/Users/zero/.openclaw/workspace"

# 1. 将根目录下的散落章节文件移动到正确的位置
echo "整理根目录散落的章节文件..."

# 移动第38章到正确位置
if [ -f "万界神级系统第38章_高维世界的真相.md" ]; then
    mv "万界神级系统第38章_高维世界的真相.md" "万界神级系统/chapters/volume1/"
    echo "✅ 移动第38章到volume1"
fi

# 移动第44章到正确位置
if [ -f "万界神级系统第44章.md" ]; then
    mv "万界神级系统第44章.md" "万界神级系统/chapters/volume1/"
    echo "✅ 移动第44章到volume1"
fi

# 移动第68章到正确位置
if [ -f "万界神级系统第68章.md" ]; then
    mv "万界神级系统第68章.md" "万界神级系统/chapters/volume1/"
    echo "✅ 移动第68章到volume1"
fi

# 移动第83章到正确位置
if [ -f "万界神级系统第83章.md" ]; then
    mv "万界神级系统第83章.md" "万界神级系统/chapters/volume1/"
    echo "✅ 移动第83章到volume1"
fi

# 2. 将优化方案文件移动到docs/planning目录
echo "整理优化方案文档..."

if [ -f "万界神级系统优化方案.md" ]; then
    mv "万界神级系统优化方案.md" "万界神级系统/docs/planning/"
    echo "✅ 移动优化方案到docs/planning"
fi

if [ -f "万界神级系统创作优化执行计划.md" ]; then
    mv "万界神级系统创作优化执行计划.md" "万界神级系统/docs/planning/"
    echo "✅ 移动创作优化执行计划到docs/planning"
fi

if [ -f "万界神级系统第57章创作专家协作优化方案.md" ]; then
    mv "万界神级系统第57章创作专家协作优化方案.md" "万界神级系统/docs/planning/"
    echo "✅ 移动第57章优化方案到docs/planning"
fi

if [ -f "万界神级系统第90章优化执行方案.md" ]; then
    mv "万界神级系统第90章优化执行方案.md" "万界神级系统/docs/planning/"
    echo "✅ 移动第90章优化方案到docs/planning"
fi

# 3. 整理万界神级系统文件夹内的临时文件
echo "整理万界神级系统文件夹内的临时文件..."

cd 万界神级系统

# 移动JSON反馈报告到docs/feedback
if [ -d "反馈报告" ]; then
    mv 反馈报告/* docs/feedback/ 2>/dev/null || true
    rmdir 反馈报告 2>/dev/null || true
    echo "✅ 整理反馈报告"
fi

# 移动JSON文件到docs/feedback
mv 第31章反馈报告_*.json docs/feedback/ 2>/dev/null || true
echo "✅ 移动JSON反馈报告"

# 移动监控脚本到docs/reports
mv 反馈监控执行脚本.py 启动反馈监控.sh 实时监控仪表板.md docs/reports/ 2>/dev/null || true
echo "✅ 移动监控脚本和仪表板"

# 移动进度文档到docs/reports
mv 100章自主创作进度.md 创作进度.md docs/reports/ 2>/dev/null || true
echo "✅ 移动进度文档"

# 清理__pycache__目录
rm -rf __pycache__ 2>/dev/null || true
echo "✅ 清理__pycache__目录"

# 4. 检查chapters目录结构
echo "检查chapters目录结构..."
cd chapters

# 确保所有volume目录存在
mkdir -p volume1 volume2 volume3 volume4

# 统计各卷的章节数量
echo "各卷章节统计："
for vol in volume1 volume2 volume3 volume4; do
    count=$(ls "$vol"/*.md 2>/dev/null | wc -l)
    echo "$vol: $count章"
done

echo "✅ 文件夹彻底整理完成！"

# 5. 返回根目录检查最终状态
cd "/Users/zero/.openclaw/workspace"
echo ""
echo "最终根目录状态："
ls -la | grep "万界神级系统" | wc -l
echo "个万界神级系统相关文件/文件夹"