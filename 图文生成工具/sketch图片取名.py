# 这个 Python 脚本属于文件管理和批量重命名工具。它主要用于自动化地批量重命名文件，适用于以下场景：
# 1.
# 纯数字序列：使用
# sequence
# 变量生成纯数字序列号，每处理一个文件就递增
# sequence。
# 2.
# 文件扩展名保持不变：只替换文件的名称部分，不改变扩展名。
# 3.
# 防止文件名冲突：在命名之前检查
# new_file_path
# 是否已存在，如果存在，则递增序列号直到找到未使用的文件名。

import os
def rename_files_with_pure_sequence(folder_path):
    """
    遍历文件夹中的文件，使用纯数字序列（如1, 2, 3等）重命名文件。

    参数：
        folder_path (str): 文件夹路径
    """
    files = os.listdir(folder_path)
    files.sort()  # 确保文件按顺序处理
    sequence = 1  # 从1开始的序列号

    for filename in files:
        # 获取文件的完整路径
        file_path = os.path.join(folder_path, filename)

        # 跳过子文件夹，仅处理文件
        if not os.path.isfile(file_path):
            continue

        # 获取文件扩展名
        _, ext = os.path.splitext(filename)

        # 生成新文件名（纯数字序列）
        new_name = f"{sequence}{ext}"
        new_file_path = os.path.join(folder_path, new_name)

        # 检查是否有重名的文件，防止覆盖
        while os.path.exists(new_file_path):
            sequence += 1
            new_name = f"{sequence}{ext}"
            new_file_path = os.path.join(folder_path, new_name)

        # 重命名文件
        os.rename(file_path, new_file_path)
        print(f"重命名: {filename} -> {new_name}")

        # 更新序列号
        sequence += 1


# 设置文件夹路径
folder_path = "/Users/jianxinwei/Desktop/苹果13尺寸图"
rename_files_with_pure_sequence(folder_path)
