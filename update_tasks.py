#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务数据更新脚本
"""

import json
from datetime import datetime

def update_task_progress(task_id, progress, status=None, outputs=None):
    """更新任务进度"""
    try:
        with open('task_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if task_id in data:
            task = data[task_id]
            task['progress'] = progress
            if status:
                task['status'] = status
            if outputs:
                # 避免重复添加
                existing_outputs = set(task.get('outputs', []))
                for output in outputs:
                    if output not in existing_outputs:
                        task['outputs'].append(output)
            task['updated_at'] = defult_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 更新统计
            total_tasks = len([k for k in data.keys() if k.startswith('task_')])
            completed_tasks = len([t for t in data.values() if t.get('status') == '已完成'])
            data['total_tasks'] = total_tasks
            data['completed_tasks'] = completed_tasks
            
            # 保存数据
            with open('task_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f'✅ 任务 {task_id} 已更新：{progress}% - {status or "无状态"}')
            print(f'📊 总任务：{total_tasks}，已完成：{completed_tasks}，完成率：{completed_tasks/total_tasks*100:.1f}%')
            return True
    except Exception as e:
        print(f'❌ 更新失败：{e}')
        return False

def complete_task(task_id, actual_duration=""):
    """完成任务"""
    return update_task_progress(task_id, 100, '已完成', [])

def create_task(title, description, priority='中', estimated_duration='未知'):
    """创建新任务"""
    try:
        with open('task_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        task_id = f"task_{len([k for k in data.keys() if k.startswith('task_')]) + 1:03d}"
        
        new_task = {
            'id': task_id,
            'title': title,
            'description': description,
            'status': '进行中',
            'priority': '优先级',
            'progress': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estimated_duration': estimated_duration,
            'actual_duration': '',
            'next_steps': [],
            'blockers': [],
            'outputs': []
        }
        
        data[task_id] = new_task
        data['current_task_id'] = task_id
        
        # 更新统计
        total_tasks = len([k for k in data.keys() if k.startswith('task_')])
        completed_tasks = len([t for t in data.values() if t.get('status') == '已完成'])
        data['total_tasks'] = total_tasks
        data['completed_tasks'] = completed_tasks
        
        with open('task_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'✅ 创建任务：{task_id} - {title}')
        print(f'📊 总任务：{total_tasks}，已完成：{completed_tasks}，完成率：{completed_tasks/total_tasks*100:.1f}%')
        return task_id
    except Exception as e:
        print(f'❌ 创建任务失败：{e}')
        return None

def get_task_status(task_id):
    """获取任务状态"""
    try:
        with open('task_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if task_id in data:
            task = data[task_id]
            return {
                'title': task['title'],
                'status': task['status'],
                'progress': task['progress'],
                'created_at': task['created_at'],
                'updated_at': task['updated_at'],
                'outputs': task.get('outputs', [])
            }
        return None
    except Exception as e:
        print(f'❌ 获取任务状态失败：{e}')
        return None

def list_tasks(status=None):
    """列出所有任务"""
    try:
        with open('task_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tasks = list(data.values())
        if status:
            tasks = [t for t in tasks if t.get('status') == status]
        
        return tasks
    except Exception as e:
        print(f'❌ 列出任务失败：{e}')
        return []

if __name__ == '__main__':
    # 测试功能
    print('🧪 任务数据更新脚本')
    
    # 测试更新
    update_task_progress('task_004', 75, '已完成', ['测试输出'])
    
    # 测试获取状态
    status = get_task_status('task_004')
    if status:
        print(f'📊 任务状态：{status}')
    
    # 测试列出任务
    tasks = list_tasks()
    print(f'📋 任务列表：{len(tasks)}个')