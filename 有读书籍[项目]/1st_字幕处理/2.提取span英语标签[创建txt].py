import os
from bs4 import BeautifulSoup


def extract_english_text_with_bs4(html_content):
    """使用 BeautifulSoup 从指定的 p#introText 标签中提取 <span class="english"> 标签内的英文内容"""
    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找 p 标签，其 id 是 introText
    p_tag = soup.find('p', id='introText')

    # 提取 p 标签内所有 class 为 english 的 span 标签内容
    if p_tag:
        english_spans = p_tag.find_all('span', class_='english')

        # 获取每个 span 标签内的文本
        extracted_text = [span.get_text(strip=True) for span in english_spans]

        # 将提取的内容用 \n\n 连接，并在每个段落之间插入空行
        return '\n\n'.join(extracted_text)
    else:
        return "未找到指定的 <p> 标签。"


def process_html(file_path):
    """处理单个HTML文件，提取英文内容并保存为同名文本文件"""
    # 读取HTML文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 提取 <span class="english"> 中的英文内容
    extracted_text = extract_english_text_with_bs4(html_content)

    # 将提取的结果保存到新文件，文件名保持一致，扩展名为 .txt
    output_file_path = file_path.replace(".html", ".txt")  # 修改文件扩展名
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(extracted_text)  # 写入提取的内容

    print(f"提取完成，新文件已生成：{output_file_path}")


def process_all_html_files_in_directory(directory_path):
    """遍历指定目录，处理所有HTML文件"""
    for root, dirs, files in os.walk(directory_path):  # 遍历目录
        for file in files:
            if file.endswith('.html'):  # 只处理以 .html 结尾的文件
                file_path = os.path.join(root, file)  # 获取文件的完整路径
                process_html(file_path)  # 处理当前HTML文件

# 输入要提取的路径
# 这里很重要,一定要写对

# 指定包含HTML文件的目录路径
html_directory_path = '/Users/jianxinwei/Pycharm/书本朗读[英语]/holybible故事书/html/books/school/Growing_in_faith_and_charcter/list_html'

# 执行HTML文件的处理
process_all_html_files_in_directory(html_directory_path)