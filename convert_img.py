import os
import re
from bs4 import BeautifulSoup

def convert_img_tags_and_punctuations(content):
    """
    替换 <img> 标签为 Markdown 图片语法，并替换指定的中文标点符号为英文符号。
    """
    # 定义中文标点替换字典
    punctuations = {
        '。': '.',  # 中文句号
        '，': ',',  # 中文逗号
        '（': '(',  # 中文左括号
        '）': ')',  # 中文右括号
        '；': ';',  # 中文分号
        '：': ':',  # 中文冒号
        '“': '"',  # 中文左引号
        '”': '"',  # 中文右引号
        '‘': "'",  # 中文左单引号
        '’': "'",  # 中文右单引号
        '《': '<',  # 中文左书名号
        '》': '>',  # 中文右书名号
        '？': '?',  # 中文问号
        '！': '!',  # 中文感叹号
        '【': '[',  # 中文左中括号
        '】': ']',  # 中文右中括号
        '｛': '{',  # 中文左大括号
        '｝': '}',  # 中文右大括号
        '—': '-',  # 中文破折号
        '～': '~',  # 中文波浪号
        '·': '.'   # 中英文顿号转换为英文句号
    }

    # 创建中文标点的正则模式
    punctuation_pattern = re.compile('|'.join(re.escape(k) for k in punctuations.keys()))

    # 替换中文标点
    content = punctuation_pattern.sub(lambda m: punctuations[m.group()], content)

    # 替换 <img> 标签为 Markdown 图片语法
    img_tag_pattern = re.compile(
        r'<img\s+[^>]*src="([^"]+)"\s+alt="([^"]*)"\s*[^>]*>', re.IGNORECASE)

    def replace_img(match):
        src = match.group(1)
        alt = match.group(2)
        return f'![{alt}]({src})'

    content = img_tag_pattern.sub(replace_img, content)

    return content

def fix_unclosed_tags(content):
    """
    使用 BeautifulSoup 自动修复未闭合的 HTML 标签。
    """
    soup = BeautifulSoup(content, 'html.parser')
    return str(soup)

def process_markdown_file(file_path):
    """
    处理单个 Markdown 文件：替换图片标签、替换标点、修复未闭合标签。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配代码块（``` 或 ~~~）
    code_block_pattern = re.compile(r'(```|~~~)([\s\S]*?)(\1)', re.MULTILINE)

    # 分割内容为代码块和非代码块
    parts = code_block_pattern.split(content)

    # 处理非代码块部分（索引为0,4,8,...）
    for i in range(0, len(parts), 4):
        if i < len(parts):
            text = parts[i]
            # 替换 <img> 标签和中文标点
            text = convert_img_tags_and_punctuations(text)
            # 使用 BeautifulSoup 修复未闭合的 HTML 标签
            text = fix_unclosed_tags(text)
            parts[i] = text

    # 重新组合内容
    new_content = ''
    for i in range(0, len(parts), 4):
        if i < len(parts):
            new_content += parts[i]
        if i + 1 < len(parts) and i + 2 < len(parts):
            new_content += parts[i + 1] + parts[i + 2] + parts[i + 3]

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def process_markdown_files():
    """
    递归处理 'docs' 目录下的所有 Markdown 文件。
    """
    target_directory = 'docs'  # 固定处理的目录

    if not os.path.isdir(target_directory):
        print(f'错误: 目录 "{target_directory}" 不存在或不是一个目录。')
        return

    for root, _, files in os.walk(target_directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_markdown_file(file_path)
                print(f'已处理: {file_path}')

if __name__ == '__main__':
    process_markdown_files()
    print('所有文件已处理完成。')