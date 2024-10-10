

import os  # 导入操作系统模块，用于文件和目录操作
import re  # 导入正则表达式模块，用于提取文件名中的数字


def find_files(directory, extensions):
    """
    在指定目录及其子目录中查找指定扩展名的文件。

    参数：
        directory (str): 要搜索的目录路径。
        extensions (tuple): 要搜索的文件扩展名（可以是多个）。

    返回：
        list: 符合条件的文件名列表。
    """
    files = []  # 初始化文件列表，用于存储找到的文件名
    # 使用 os.walk 遍历目录及其子目录
    for root, dirs, file_names in os.walk(directory):
        for file_name in file_names:
            # 如果文件名符合指定扩展名之一，则添加到文件列表中
            if file_name.endswith(extensions):
                files.append(file_name)  # 只保存文件名，不包含路径
    return files


def sort_files_numerically(file_list):
    """
    按照文件名中的数字对文件列表进行排序。

    参数：
        file_list (list): 要排序的文件名列表。

    返回：
        list: 按数字顺序排序后的文件名列表。
    """

    # 使用正则表达式提取文件名中的数字
    def extract_number(file_name):
        match = re.search(r'(\d+)', file_name)  # 搜索文件名中的数字部分
        return int(match.group(1)) if match else float('inf')  # 如果找到数字则返回数字，否则返回无穷大，将无数字的文件放在最后

    # 按提取的数字对文件名进行排序
    return sorted(file_list, key=extract_number)


# 在代码中指定路径和文件类型
current_directory = "/Users/jianxinwei/Pycharm/tset/output/又"  # 替换为你要搜索的目录路径
file_extensions = ('.txt', '.mp3')  # 替换为你想查找的文件类型，可以添加更多类型

# 检查指定的路径是否有效
if not os.path.isdir(current_directory):
    print(f"指定的路径无效: {current_directory}")
else:
    # 查找指定目录及其子目录中的指定扩展名文件
    files_array = find_files(current_directory, file_extensions)  # 查找指定类型的文件

    # 按数字顺序排序文件名
    files_array_sorted = sort_files_numerically(files_array)  # 对文件按数字顺序排序

    # 打印排序后的文件数组
    print("文件数组（按数字排序）:", files_array_sorted)