#!/usr/bin/env python3

from task_manager import create_task, start_task, update_progress, add_output, complete_task

# 创建调研任务
task_id = create_task(
    "调研任务状态推送最佳实践", 
    "调研GitHub Actions、webhooks、独立页面等任务状态推送的最佳实践和高星开源项目",
    priority="高",
    estimated_duration="30-45分钟"
)

# 开始任务
start_task(task_id)

# 更新进度
update_progress(25)
add_output("完成初步调研报告，分析了主流推送方案")

print(f"任务已创建并开始，任务ID: {task_id}")
print("请查看 '任务状态看板.md' 文件获取实时状态")