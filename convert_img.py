import os
import re
from bs4 import BeautifulSoup

def convert_img_tags_to_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(content, 'html.parser')
    imgs = soup.find_all('img')

    for img in imgs:
        src = img.get('src', '')
        alt = img.get('alt', '')
        # 构建 Markdown 图片语法
        markdown_img = f'![{alt}]({src})'
        # 替换 HTML <img> 标签为 Markdown 图片语法
        img.replace_with(markdown_img)

    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        # 使用 prettify 可能会改变文件的格式，这里直接使用 str(soup) 保持原有格式
        file.write(str(soup))

def process_markdown_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                convert_img_tags_to_markdown(file_path)
                print(f'已转换: {file_path}')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='递归转换 Markdown 文件中的 HTML <img> 标签为 Markdown 图片语法。')
    parser.add_argument('directory', type=str, help='要处理的目标目录路径')

    args = parser.parse_args()
    target_directory = args.directory

    if not os.path.isdir(target_directory):
        print(f'错误: 目录 "{target_directory}" 不存在或不是一个目录。')
    else:
        process_markdown_files(target_directory)
        print('所有文件已处理完成。')