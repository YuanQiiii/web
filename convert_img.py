import os
import re

def convert_img_tags_and_punctuations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配代码块（``` 或 ~~~）
    code_block_pattern = re.compile(r'(```|~~~)([\s\S]*?)(\1)', re.MULTILINE)

    # 分割内容为代码块和非代码块
    parts = code_block_pattern.split(content)

    # 定义中文标点替换字典
    punctuations = {
        '。': '.',
        '，': ',',
        '（': '(',
        '）': ')',
        '；': ';',
        '：': ':',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '《': '<',
        '》': '>',
        '？': '?',
        '！': '!',
        '【': '[',
        '】': ']',
        '｛': '{',
        '｝': '}',
        '—': '-',
        '～': '~',
        '·': '.'
    }

    # 创建中文标点的正则模式
    punctuation_pattern = re.compile('|'.join(re.escape(k) for k in punctuations.keys()))

    # 处理非代码块部分（索引为0,4,8,...）
    for i in range(0, len(parts), 4):
        if i < len(parts):
            text = parts[i]
            # 替换 <img> 标签为 Markdown 图片语法
            img_tag_pattern = re.compile(
                r'<img\s+[^>]*src="([^"]+)"\s+alt="([^"]*)"\s*[^>]*>', re.IGNORECASE)
            
            def replace_img(match):
                src = match.group(1)
                alt = match.group(2)
                return f'![{alt}]({src})'
            
            text = img_tag_pattern.sub(replace_img, text)
            
            # 替换中文标点
            text = punctuation_pattern.sub(lambda m: punctuations[m.group()], text)
            
            parts[i] = text

    # 重新组合内容
    new_content = ''
    for i in range(0, len(parts), 4):
        if i < len(parts):
            new_content += parts[i]
        if i + 1 < len(parts) and i + 2 < len(parts):
            new_content += parts[i + 1] + parts[i + 2] + parts[i + 3]

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def process_markdown_files():
    target_directory = 'docs'  # 固定处理的目录

    if not os.path.isdir(target_directory):
        print(f'错误: 目录 "{target_directory}" 不存在或不是一个目录。')
        return

    for root, _, files in os.walk(target_directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                convert_img_tags_and_punctuations(file_path)
                print(f'已转换: {file_path}')

if __name__ == '__main__':
    process_markdown_files()
    print('所有文件已处理完成。')