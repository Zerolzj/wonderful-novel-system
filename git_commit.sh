#!/bin/bash

# Git操作脚本 - 用于自动提交小说章节更新

# 设置变量
REPO_DIR="/Users/zero/.openclaw/workspace"
COMMIT_MSG_PREFIX="《万界神级系统》更新"

# 函数：添加并提交文件
git_commit_update() {
    local file_path="$1"
    local chapter_number="$2"
    local chapter_title="$3"
    
    cd "$REPO_DIR"
    
    # 添加文件到暂存区
    git add "$file_path"
    
    # 检查是否有变化
    if git diff --cached --quiet; then
        echo "文件 $file_path 没有变化，跳过提交"
        return 1
    fi
    
    # 提交变化
    local commit_msg="$COMMIT_MSG_PREFIX - 第${chapter_number}章：${chapter_title}"
    git commit -m "$commit_msg"
    
    echo "已提交：$commit_msg"
    return 0
}

# 函数：推送更改
git_push_updates() {
    cd "$REPO_DIR"
    
    # 推送到远程仓库
    git push origin main
    
    echo "已推送到远程仓库"
}

# 函数：初始化仓库（如果需要）
git_init_repo() {
    cd "$REPO_DIR"
    
    # 检查是否已经是git仓库
    if [ ! -d ".git" ]; then
        git init
        echo "已初始化Git仓库"
    fi
    
    # 检查是否有远程仓库
    if ! git remote get-url origin >/dev/null 2>&1; then
        echo "请添加远程仓库：git remote add origin <你的GitHub仓库URL>"
        return 1
    fi
    
    return 0
}

# 函数：创建章节提交
commit_chapter() {
    local chapter_file="$1"
    local chapter_num=$(echo "$chapter_file" | grep -o '[0-9]\+' | head -1)
    local chapter_title=$(grep "^# " "$chapter_file" | head -1 | sed 's/^# //')
    
    if [ -z "$chapter_num" ] || [ -z "$chapter_title" ]; then
        echo "无法解析章节信息：$chapter_file"
        return 1
    fi
    
    git_commit_update "$chapter_file" "$chapter_num" "$chapter_title"
}

# 主函数
main() {
    case "$1" in
        "init")
            git_init_repo
            ;;
        "commit")
            if [ -z "$2" ]; then
                echo "用法: $0 commit <文件路径>"
                exit 1
            fi
            commit_chapter "$2"
            ;;
        "push")
            git_push_updates
            ;;
        "status")
            cd "$REPO_DIR"
            git status
            ;;
        "help")
            echo "用法:"
            echo "  $0 init                    - 初始化Git仓库"
            echo "  $0 commit <文件路径>        - 提交章节文件"
            echo "  $0 push                    - 推送到远程仓库"
            echo "  $0 status                  - 查看Git状态"
            ;;
        *)
            echo "未知命令: $1"
            echo "使用 '$0 help' 查看帮助"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"