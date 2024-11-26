import os

# html符号修改成正常符号
def replace_html_entities(content):
    # 定义要替换的HTML实体和对应的符号
    html_entities = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&#39;': "'",
        # 添加其他需要替换的实体
    }
    for entity, char in html_entities.items():
        content = content.replace(entity, char)
    return content

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        updated_content = replace_html_entities(content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"已处理文件: {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def recursive_process(directory):
    if not os.path.isdir(directory):
        print(f"目录 {directory} 不存在。")
        return
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    target_directory = 'docs'  # 指定为docs目录
    recursive_process(target_directory)