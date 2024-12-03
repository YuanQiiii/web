```sh
ls -l  # 以长格式列出文件和目录
ls -a  # 显示所有文件，包括隐藏文件

cd /path/to/directory  # 切换到指定目录
cd ..  # 返回上一级目录
cd ~  # 返回到家目录

pwd  # 显示当前完整路径

cp source_file destination_file  # 复制文件
cp -r source_directory destination_directory  # 递归复制目录

mv old_name new_name  # 重命名文件
mv file /path/to/directory  # 移动文件到指定目录

rm filename  # 删除文件
rm -r directory_name  # 递归删除目录
rm -f filename  # 强制删除文件，不提示确认

mkdir new_directory  # 创建新目录
mkdir -p /path/to/new/directory  # 创建多级目录结构

rmdir directory_name  # 删除空目录

touch new_file  # 创建空文件

chmod 755 filename  # 设置文件权限为读/写/执行
chmod -R 644 directory_name  # 递归设置目录权限

chown user:group filename  # 更改文件的所有者和组

grep "text" file  # 在文件中搜索文本

find / -name filename  # 在根目录下搜索名为filename的文件

tar -cvf archive_name.tar directory_name  # 创建一个tar包
tar -xvf archive_name.tar  # 解压一个tar包

gzip file  # 压缩文件
gunzip file.gz  # 解压文件

du -sh directory_name  # 显示目录的总大小

df -h  # 显示文件系统的磁盘空间使用情况

top  # 实时显示进程信息

ps aux  # 显示所有进程信息

kill PID  # 终止指定PID的进程

man command_name # 查看特定命令的手册页
```

