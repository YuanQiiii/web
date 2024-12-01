from bs4 import BeautifulSoup

def remove_images_in_content():
    # 读取HTML文件
    with open('qblog.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到所有class为content的div
    content_divs = soup.find_all('div', class_='content')

    # 遍历每个content div
    for content_div in content_divs:
        # 找到并删除其中的image div
        image_divs = content_div.find_all('div', class_='image')
        for image_div in image_divs:
            image_div.decompose()

    # 保存修改后的文件
    with open('qblog_cleaned.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

if __name__ == "__main__":
    remove_images_in_content()