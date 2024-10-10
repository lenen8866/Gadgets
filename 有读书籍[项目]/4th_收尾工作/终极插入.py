
import os
from bs4 import BeautifulSoup

# 指定包含a.html文件的文件夹路径
a_folder_path = '../../tempbak/[07:4th:2生成:span_to_br'
# 指定包含b.html文件的文件夹路径
b_folder_path = '/Users/jianxinwei/Pycharm/书本朗读[英语]/holybible故事书/html/books/school/Growing_in_faith_and_charcter/list_html'

# 遍历a_folder_path文件夹中的每个a.html文件
for a_filename in os.listdir(a_folder_path):
    if a_filename.endswith('.html'):
        # 构造a.html和b.html的完整路径
        a_file_path = os.path.join(a_folder_path, a_filename)
        b_file_path = os.path.join(b_folder_path, a_filename)

        # 检查b.html文件是否存在
        if os.path.exists(b_file_path):
            # 读取a.html文件内容
            with open(a_file_path, 'r', encoding='utf-8') as file:
                a_content = file.read()

            # 解析a.html但只获取内容，不对其进行任何修改
            soup_a = BeautifulSoup(a_content, 'html.parser')
            content_a = soup_a.find('div', class_='content').decode_contents()

            # 读取b.html文件内容
            with open(b_file_path, 'r', encoding='utf-8') as file:
                b_content = file.read()

            # 解析b.html
            soup_b = BeautifulSoup(b_content, 'html.parser')

            # 找到b.html中的<div class="content">
            content_b = soup_b.find('div', class_='content')

            # 替换b.html中<div class="content">的内部内容
            if content_b:
                content_b.clear()  # 清除b.html中<div>的现有内容
                content_b.append(BeautifulSoup(content_a, 'html.parser'))  # 将a.html的内容添加到b.html

            # 保存修改后的b.html
            with open(b_file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup_b))

            print(f'Processed {b_file_path} successfully.')
        else:
            print(f'{b_file_path} does not exist.')