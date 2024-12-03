#!/bin/bash

# 检查并设置执行权限
if [ ! -x "$0" ]; then
    echo "添加执行权限..."
    chmod +x "$0"
fi

echo "启动ppemail.py守护进程..."

# 使用nohup启动监控进程
if ! ps aux | grep -v grep | grep "ppemail.py" > /dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 首次启动 ppemail.py"
    nohup python3 ppemail.py > ppemail.log 2>&1 &
fi

# 使用nohup启动监控循环
nohup bash -c '
while true; do
    if ! ps aux | grep -v grep | grep "ppemail.py" > /dev/null; then
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] 重启 ppemail.py" >> ppemail.log
        python3 ppemail.py >> ppemail.log 2>&1 &
    fi
    sleep 30
done' > monitor.log 2>&1 &

echo "守护进程已在后台启动"
echo "查看日志: tail -f ppemail.log"
echo "查看监控日志: tail -f monitor.log"