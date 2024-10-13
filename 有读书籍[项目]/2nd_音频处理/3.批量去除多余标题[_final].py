import os
import re

# 定义要删除的关键词列表
keywords_to_remove = ['_final']
# keywords_to_remove = ['关键词1', '关键词2', 'Keyword3']

# 定义要处理的文件扩展名列表
allowed_extensions = ['.txt', '.html', '.mp3']

# 函数：删除标题中的关键词
def remove_keywords_from_title(title, keywords):
    # 遍历关键词并删除出现在标题中的每个关键词
    for keyword in keywords:
        title = re.sub(re.escape(keyword), '', title, flags=re.IGNORECASE)  # 忽略大小写删除
    return title.strip()  # 删除多余空格并返回

# 函数：批量重命名文件
def batch_rename_files(directory, keywords):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(directory):
        # 获取文件的完整路径
        file_path = os.path.join(directory, filename)

        # 仅处理文件而非文件夹
        if os.path.isfile(file_path):
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)

            # 检查文件扩展名是否在允许列表中
            if ext.lower() in allowed_extensions:
                # 删除文件名中的关键词
                new_name = remove_keywords_from_title(name, keywords)

                # 创建新的完整文件路径
                new_file_path = os.path.join(directory, new_name + ext)

                # 重命名文件
                os.rename(file_path, new_file_path)
                print(f"文件重命名为: {new_file_path}")

# 示例用法
input_directory = '../../tempbak/[03]_2nd:2生成:完整音频mp3[放Lrc文件]'
batch_rename_files(input_directory, keywords_to_remove)
print("批量重命名完成。")