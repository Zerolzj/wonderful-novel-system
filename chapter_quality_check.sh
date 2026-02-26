#!/bin/bash

# 章节质量检查脚本
# 检查每章字数、代码修仙元素、人物成长线、爽点设置

echo "开始章节质量检查..."
echo "=============================="

# 获取所有章节文件
chapters=$(find /Users/zero/.openclaw/workspace/万界神级系统 -name "第*.md" -type f | grep -v "创作中" | grep -v "反馈" | grep -v "进度" | sort -V)

# 统计变量
total_chapters=0
qualified_chapters=0
quality_issues=""

for chapter in $chapters; do
    chapter_name=$(basename "$chapter" .md)
    
    # 检查文件是否存在
    if [ ! -f "$chapter" ]; then
        echo "❌ $chapter_name - 文件不存在"
        continue
    fi
    
    # 统计中文字数（排除标点符号和代码块）
    word_count=$(grep -v '```' "$chapter" | sed 's/[，。！？；：""''（）《》【】、]//g' | grep -o '[\u4e00-\u9fa5]' | wc -l | tr -d ' ')
    
    # 检查代码修仙元素
    code_elements=$(grep -c "代码\|系统\|函数\|算法\|编程\|数据\|逻辑\|循环\|条件\|变量\|数组\|对象\|类\|方法\|接口\|API\|JSON\|HTML\|CSS\|JavaScript\|Python\|Java\|C++\|SQL\|数据库\|框架\|库\|包\|模块\|调试\|测试\|优化\|重构\|部署\|版本控制" "$chapter" 2>/dev/null || echo "0")
    
    # 检查修仙元素
    cultivation_elements=$(grep -c "修仙\|灵气\|功法\|境界\|突破\|炼丹\|炼器\|阵法\|符箓\|丹药\|灵石\|法宝\|洞府\|宗门\|师父\|师兄\|师姐\|师弟\|师妹\|长老\|宗主\|天劫\|飞升\|仙界\|人间\|魔界\|妖界\|神界\|道心\|悟道\|修行\|修炼\|真元\|元神\|金丹\|元婴\|化神\|返虚\|合体\|大乘\|渡劫" "$chapter" 2>/dev/null || echo "0")
    
    # 检查人物成长相关词汇
    growth_elements=$(grep -c "成长\|进步\|提升\|突破\|领悟\|学会\|掌握\|熟练\|精通\|创新\|改进\|完善\|升级\|进化\|蜕变\|飞跃\|超越\|战胜\|击败\|克服\|解决\|应对\|适应\|改变" "$chapter" 2>/dev/null || echo "0")
    
    # 检查爽点元素
    exciting_elements=$(grep -c "震撼\|惊人\|不可思议\|难以置信\|令人惊叹\|震撼人心\|惊心动魄\|热血沸腾\|激动人心\|痛快\|爽快\|过瘾\|解气\|扬眉吐气\|一鸣惊人\|大放异彩\|脱颖而出\|技惊四座\|震惊全场\|全场沸腾\|掌声雷动\|欢呼声\|赞叹声" "$chapter" 2>/dev/null || echo "0")
    
    total_chapters=$((total_chapters + 1))
    
    # 质量判断
    is_qualified=true
    issues=""
    
    # 字数检查
    if [ "$word_count" -lt 3000 ]; then
        is_qualified=false
        issues="${issues}字数不足(${word_count}字); "
    elif [ "$word_count" -gt 4000 ]; then
        is_qualified=false
        issues="${issues}字数过多(${word_count}字); "
    fi
    
    # 元素检查
    if [ "$code_elements" -lt 5 ]; then
        is_qualified=false
        issues="${issues}代码元素不足(${code_elements}处); "
    fi
    
    if [ "$cultivation_elements" -lt 5 ]; then
        is_qualified=false
        issues="${issues}修仙元素不足(${cultivation_elements}处); "
    fi
    
    if [ "$growth_elements" -lt 3 ]; then
        is_qualified=false
        issues="${issues}成长元素不足(${growth_elements}处); "
    fi
    
    if [ "$exciting_elements" -lt 2 ]; then
        is_qualified=false
        issues="${issues}爽点不足(${exciting_elements}处); "
    fi
    
    # 输出结果
    if [ "$is_qualified" = true ]; then
        echo "✅ $chapter_name - 合格 (${word_count}字)"
        qualified_chapters=$((qualified_chapters + 1))
    else
        echo "❌ $chapter_name - 不合格: ${issues}"
        quality_issues="${quality_issues}$chapter_name: ${issues}\n"
    fi
done

echo "=============================="
echo "检查完成！"
echo "总章节数: $total_chapters"
echo "合格章节: $qualified_chapters"
echo "合格率: $(( qualified_chapters * 100 / total_chapters ))%"

if [ -n "$quality_issues" ]; then
    echo -e "\n质量问题详情:"
    echo -e "$quality_issues"
fi

# 保存检查结果到日志
echo "$(date): 章节质量检查完成 - 总计${total_chapters}章，合格${qualified_chapters}章，合格率$(( qualified_chapters * 100 / total_chapters ))%" >> /Users/zero/.openclaw/workspace/memory/2026-02-26.md