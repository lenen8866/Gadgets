"""
╔═════════════════════════════════════════════════════╗
║     L          EEEE    N   N    EEEE    N   N       ║
║     L          E       NN  N    E       NN  N       ║
║     L          EEEE    N N N    EEEE    N N N       ║
║     L          E       N  NN    E       N  NN       ║
║     LLLLL      EEEE    N   N    EEEE    N   N       ║
╚═════════════════════════════════════════════════════╝
     # Created by Lenen at  10/5/24  [MM-DD-YY]
文档:
支持递归遍历(子目录)切割
你只需要改动1个参数即可:

input_directory = "./文件"  # 替换为你的输入目录路径(支持递归)

下面是默认:
output_directory = "./output"  # 替换为你想要保存输出文件的目录路径,(如果没有,则新创建)

 if char_count + len(line) + 1 > 1000:(默认是1000)
if file_name.endswith(('.txt', '.lrc')):默认txt,和lrc,
"""

import os

def split_story(file_path, output_dir):
    # 打开并读取文件内容
    with open(file_path, "r", encoding="utf-8") as f:
        story = f.read()

    # 将文件内容按行分割
    lines = story.split('\n')
    accumulated_text = ""  # 用于存储累积的文本块
    file_count = 1  # 用于命名分割后的文件，起始序号为1
    char_count = 0  # 用于统计当前文本块的字符数

    # 确保输出目录存在，如果不存在则创建
    if not os.path.exists(output_dir):  # 检查输出目录是否存在
        os.makedirs(output_dir)  # 如果不存在，创建该目录

    # 根据N字符的限制，创建分割后的文本文件(这里填写切割的字符串)
    for line in lines:
        # 如果累积字符数加上当前行字符数（包括换行符）超过1000，则保存当前累积的文本到新文件
        if char_count + len(line) + 1 > 1000:  # +1 是为了考虑换行符
            # 创建分割后的文件名：原文件名_part_序号.txt
            output_file = os.path.join(output_dir, f"{os.path.basename(file_path).split('.')[0]}_part_{file_count}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(accumulated_text)

            # 重置累积变量以准备下一文件
            accumulated_text = line + "\n"  # 将当前行作为新文本块的起始内容
            file_count += 1  # 文件序号加1
            char_count = len(line) + 1  # 重置字符计数为当前行的字符数（包括换行符）
        else:
            # 如果字符数未超出1000，将当前行添加到累积文本块中
            accumulated_text += line + "\n"
            char_count += len(line) + 1  # 加上行的字符数和换行符

    # 保存剩余的文本到最终文件，确保没有遗漏
    if accumulated_text.strip():
        output_file = os.path.join(output_dir, f"{os.path.basename(file_path).split('.')[0]}_part_{file_count}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(accumulated_text)

def batch_process(input_dir, output_dir):
    # 遍历输入目录的所有文件和子目录
    for root, _, files in os.walk(input_dir):  # 使用 os.walk 递归遍历目录
        for file_name in files:
            # 只处理 .txt 和 .lrc 文件,(不需要哪个,删除或者增加)
            if file_name.endswith(('.txt', '.lrc')):  # 筛选符合条件的文件
                file_path = os.path.join(root, file_name)  # 获取文件的完整路径
                # 计算输出目录的子路径，以保持子目录结构
                relative_path = os.path.relpath(root, input_dir)  # 计算相对路径
                output_subdir = os.path.join(output_dir, relative_path)  # 目标输出子目录

                # 确保输出子目录存在
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                print(f"正在处理 {file_path}...")  # 打印当前处理的文件路径
                split_story(file_path, output_subdir)  # 调用分割函数
                print(f"{file_name} 处理完成。")  # 打印处理完成提示

if __name__ == "__main__":
    # 指定包含 .txt 和 .lrc 文件的输入目录
    input_directory = "./文件"  # 替换为你的输入目录路径
    # 指定用于保存分割后文件的输出目录
    output_directory = "./output"  # 替换为你想要保存输出文件的目录路径

    batch_process(input_directory, output_directory)  # 批量处理输入目录中的文件