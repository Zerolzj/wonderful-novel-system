#!/bin/bash

# 《万界神级系统》读者反馈监控启动脚本
# 专门监控第31-40章的读者反馈

echo "=== 《万界神级系统》读者反馈监控系统启动 ==="
echo "启动时间: $(date)"
echo "监控范围: 第31章-第40章"
echo "监控重点: 新世界设定接受度、代码修仙元素共鸣度"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

echo "✅ Python3 环境检查通过"

# 检查必要文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/反馈监控执行脚本.py"

if [ ! -f "$MONITOR_SCRIPT" ]; then
    echo "❌ 监控脚本不存在: $MONITOR_SCRIPT"
    exit 1
fi

echo "✅ 监控脚本检查通过"

# 创建报告目录
REPORT_DIR="$SCRIPT_DIR/反馈报告"
mkdir -p "$REPORT_DIR"
echo "✅ 报告目录已创建: $REPORT_DIR"

# 启动监控
echo ""
echo "🚀 启动读者反馈监控系统..."
echo "📊 正在分析第31章反馈数据..."
echo ""

cd "$SCRIPT_DIR"
python3 "$MONITOR_SCRIPT"

echo ""
echo "=== 监控系统运行完成 ==="
echo "报告文件保存在: $REPORT_DIR"
echo "下次自动运行时间: 1小时后"
echo ""

# 设置定时任务（如果需要）
if command -v crontab &> /dev/null; then
    echo "⏰ 设置定时监控任务..."
    
    # 创建临时crontab文件
    TEMP_CRON=$(mktemp)
    
    # 添加每小时运行一次的任务
    echo "0 * * * * cd $SCRIPT_DIR && python3 反馈监控执行脚本.py >> $REPORT_DIR/cron.log 2>&1" > "$TEMP_CRON"
    
    # 安装crontab
    crontab "$TEMP_CRON"
    rm "$TEMP_CRON"
    
    echo "✅ 定时任务已设置: 每小时运行一次"
else
    echo "⚠️  crontab 不可用，请手动设置定时任务"
fi

echo ""
echo "📋 监控系统状态:"
echo "   - 监控范围: 第31-40章"
echo "   - 当前重点: 第31章-新世界之门"
echo "   - 分析维度: 设定接受度、技术共鸣度"
echo "   - 报告频率: 每小时"
echo ""
echo "🔍 如需查看实时报告，请运行:"
echo "   python3 反馈监控执行脚本.py"
echo ""
echo "📞 紧急联系: 发现重大负面反馈时立即通知主Agent"
echo ""
echo "=== 监控系统启动完成 ==="