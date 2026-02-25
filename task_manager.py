#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务状态管理器
用于实时更新和维护任务状态看板
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    PENDING = "待开始"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    PAUSED = "已暂停"
    FAILED = "失败"
    CANCELLED = "已取消"

class TaskPriority(Enum):
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    URGENT = "紧急"

@dataclass
class Task:
    """任务数据结构"""
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    progress: int  # 0-100
    created_at: str
    updated_at: str
    estimated_duration: str  # 预计耗时
    actual_duration: str = ""
    next_steps: List[str] = None
    blockers: List[str] = None
    outputs: List[str] = None
    
    def __post_init__(self):
        if self.next_steps is None:
            self.next_steps = []
        if self.blockers is None:
            self.blockers = []
        if self.outputs is None:
            self.outputs = []

class TaskBoardManager:
    """任务看板管理器"""
    
    def __init__(self, board_file: str = "任务状态看板.md"):
        self.board_file = board_file
        self.data_file = "task_data.json"
        self.tasks: Dict[str, Task] = {}
        self.current_task_id: Optional[str] = None
        
        # 加载现有数据
        self._load_data()
    
    def _load_data(self):
        """加载任务数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for task_id, task_data in data.items():
                    task = Task(
                        id=task_data['id'],
                        title=task_data['title'],
                        description=task_data['description'],
                        status=TaskStatus(task_data['status']),
                        priority=TaskPriority(task_data['priority']),
                        progress=task_data['progress'],
                        created_at=task_data['created_at'],
                        updated_at=task_data['updated_at'],
                        estimated_duration=task_data['estimated_duration'],
                        actual_duration=task_data.get('actual_duration', ''),
                        next_steps=task_data.get('next_steps', []),
                        blockers=task_data.get('blockers', []),
                        outputs=task_data.get('outputs', [])
                    )
                    self.tasks[task_id] = task
                
                # 加载当前任务ID
                if 'current_task_id' in data:
                    self.current_task_id = data['current_task_id']
        except Exception as e:
            print(f"加载数据失败: {e}")
    
    def _save_data(self):
        """保存任务数据"""
        try:
            data = {}
            for task_id, task in self.tasks.items():
                data[task_id] = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status.value,
                    'priority': task.priority.value,
                    'progress': task.progress,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at,
                    'estimated_duration': task.estimated_duration,
                    'actual_duration': task.actual_duration,
                    'next_steps': task.next_steps,
                    'blockers': task.blockers,
                    'outputs': task.outputs
                }
            
            if self.current_task_id:
                data['current_task_id'] = self.current_task_id
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def create_task(self, title: str, description: str, priority: TaskPriority = TaskPriority.MEDIUM, 
                   estimated_duration: str = "未知") -> str:
        """创建新任务"""
        task_id = f"task_{len(self.tasks) + 1:03d}"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            priority=priority,
            progress=0,
            created_at=now,
            updated_at=now,
            estimated_duration=estimated_duration
        )
        
        self.tasks[task_id] = task
        self._save_data()
        self._update_board()
        
        return task_id
    
    def start_task(self, task_id: str) -> bool:
        """开始任务"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.IN_PROGRESS
            self.tasks[task_id].updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.current_task_id = task_id
            
            self._save_data()
            self._update_board()
            return True
        return False
    
    def update_progress(self, task_id: str, progress: int, status: TaskStatus = None):
        """更新任务进度"""
        if task_id in self.tasks:
            self.tasks[task_id].progress = min(100, max(0, progress))
            self.tasks[task_id].updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if status:
                self.tasks[task_id].status = status
            
            self._save_data()
            self._update_board()
    
    def add_output(self, task_id: str, output: str):
        """添加任务产出"""
        if task_id in self.tasks:
            self.tasks[task_id].outputs.append(output)
            self.tasks[task_id].updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self._save_data()
            self._update_board()
    
    def complete_task(self, task_id: str, actual_duration: str = ""):
        """完成任务"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.COMPLETED
            self.tasks[task_id].progress = 100
            self.tasks[task_id].updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.tasks[task_id].actual_duration = actual_duration
            
            if self.current_task_id == task_id:
                self.current_task_id = None
            
            self._save_data()
            self._update_board()
    
    def pause_task(self, task_id: str):
        """暂停任务"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.PAUSED
            self.tasks[task_id].updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if self.current_task_id == task_id:
                self.current_task_id = None
            
            self._save_data()
            self._update_board()
    
    def _update_board(self):
        """更新看板文件"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# 📋 实时任务状态看板

**最后更新时间**: {now}

## 🎯 当前任务状态
"""
        
        if self.current_task_id and self.current_task_id in self.tasks:
            current_task = self.tasks[self.current_task_id]
            content += f"""
### 🔥 正在执行：{current_task.title}

**状态**: {current_task.status.value} | **进度**: {current_task.progress}% | **优先级**: {current_task.priority.value}
**开始时间**: {current_task.created_at}
**预计耗时**: {current_task.estimated_duration}

**描述**: {current_task.description}

**下一步骤**: 
{chr(10).join(f"- {step}" for step in current_task.next_steps) if current_task.next_steps else "- 无"}

**产出物**: 
{chr(10).join(f"- {output}" for output in current_task.outputs) if current_task.outputs else "- 无"}

**阻塞因素**: 
{chr(10).join(f"- {blocker}" for blocker in current_task.blockers) if current_task.blockers else "- 无"}

---
"""
        else:
            content += """
### 📭 当前无任务执行中

---

"""
        
        # 任务列表
        content += "## 📊 所有任务概览\n\n"
        
        # 按状态分组
        status_groups = {}
        for task in self.tasks.values():
            status = task.status.value
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(task)
        
        # 显示各状态任务
        status_order = ["进行中", "待开始", "已暂停", "已完成", "失败", "已取消"]
        
        for status in status_order:
            if status in status_groups:
                content += f"### 📌 {status} ({len(status_groups[status])}个)\n\n"
                
                for task in status_groups[status]:
                    priority_emoji = {
                        "紧急": "🔴",
                        "高": "🟠", 
                        "中": "🟡",
                        "低": "🟢"
                    }.get(task.priority.value, "⚪")
                    
                    content += f"{priority_emoji} **{task.title}** - {task.progress}%\n"
                    content += f"   - ID: {task.id}\n"
                    content += f"   - 创建: {task.created_at}\n"
                    content += f"   - 预计: {task.estimated_duration}\n"
                    
                    if task.outputs:
                        content += f"   - 产出: {', '.join(task.outputs[:2])}"
                        if len(task.outputs) > 2:
                            content += f" (+{len(task.outputs)-2}个)"
                        content += "\n"
                    
                    content += "\n"
        
        # 统计信息
        content += "## 📈 统计信息\n\n"
        
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        in_progress_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
        
        content += f"- **任务总数**: {total_tasks}\n"
        content += f"- **已完成**: {completed_tasks} ({completed_tasks/total_tasks*100:.1f}%)\n"
        content += f"- **进行中**: {in_progress_tasks}\n"
        content += f"- **完成率**: {completed_tasks/total_tasks*100:.1f}%\n\n"
        
        # 使用说明
        content += """## 📝 使用说明

### 交互方式
- **查看状态**: 随时查看此文件获取最新任务状态
- **暂停任务**: 发送 "暂停" 或 "停止" 暂停当前任务
- **继续任务**: 发送 "继续 [任务ID]" 继续指定任务
- **更新进度**: 发送 "进度 [任务ID] [百分比]" 更新进度
- **完成任务**: 发送 "完成 [任务ID] [实际耗时]" 完成任务

### 状态说明
- 🔴 紧急: 需要立即处理
- 🟠 高: 优先处理
- 🟡 中: 正常处理
- 🟢 低: 有空时处理

---
*看板自动更新，最后更新时间: {now}*
"""
        
        # 写入文件
        try:
            with open(self.board_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"更新看板失败: {e}")
    
    def get_current_task(self) -> Optional[Task]:
        """获取当前任务"""
        if self.current_task_id and self.current_task_id in self.tasks:
            return self.tasks[self.current_task_id]
        return None
    
    def list_tasks(self, status: TaskStatus = None) -> List[Task]:
        """列出任务"""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks

# 全局实例
task_board = TaskBoardManager()

# 便捷函数
def create_task(title: str, description: str, priority: TaskPriority = TaskPriority.MEDIUM, 
                estimated_duration: str = "未知") -> str:
    """创建任务"""
    return task_board.create_task(title, description, priority, estimated_duration)

def start_task(task_id: str) -> bool:
    """开始任务"""
    return task_board.start_task(task_id)

def update_progress(progress: int, task_id: str = None):
    """更新进度"""
    if not task_id:
        current = task_board.get_current_task()
        if current:
            task_id = current.id
        else:
            return
    
    status = TaskStatus.IN_PROGRESS
    if progress >= 100:
        status = TaskStatus.COMPLETED
    
    task_board.update_progress(task_id, progress, status)

def add_output(output: str, task_id: str = None):
    """添加产出"""
    if not task_id:
        current = task_board.get_current_task()
        if current:
            task_id = current.id
        else:
            return
    
    task_board.add_output(task_id, output)

def complete_task(task_id: str = None, actual_duration: str = ""):
    """完成任务"""
    if not task_id:
        current = task_board.get_current_task()
        if current:
            task_id = current.id
        else:
            return
    
    task_board.complete_task(task_id, actual_duration)

def pause_task(task_id: str = None):
    """暂停任务"""
    if not task_id:
        current = task_board.get_current_task()
        if current:
            task_id = current.id
        else:
            return
    
    task_board.pause_task(task_id)

if __name__ == "__main__":
    # 示例用法
    task_id = create_task("测试任务", "这是一个测试任务", TaskPriority.HIGH, "30分钟")
    start_task(task_id)
    update_progress(50)
    add_output("测试产出")
    complete_task(task_id, "25分钟")
    
    print("任务看板已更新，请查看 '任务状态看板.md' 文件")