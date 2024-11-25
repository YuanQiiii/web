@echo off
REM 导航到项目目录
cd /d "C:\Users\exqin\Desktop\web"

REM 添加所有更改
git add .

REM 提交更改，如果没有更改则跳过提交
git commit -m "自动提交" || echo 没有更改需要提交。

REM 推送到远程仓库
git push

echo 已完成 git push.
pause