import os


def split_story(file_path, output_dir, max_chars=950):
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

    # 根据字符限制分割文件
    for line in lines:
        # 如果添加当前行会超过字符数限制，先将累积的文本写入文件
        if char_count + len(line) + 1 > max_chars:  # +1 是为了换行符
            # 写入到新的分割文件中
            output_file = os.path.join(output_dir,
                                       f"{os.path.basename(file_path).split('.')[0]}_part_{file_count}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(accumulated_text)

            # 重置变量，准备写入下一个文件
            accumulated_text = ""
            char_count = 0
            file_count += 1

        # 添加当前行到累积文本中
        accumulated_text += line + "\n"
        char_count += len(line) + 1  # 加上换行符的字符

    # 保存剩余的文本到最终文件，确保没有遗漏
    if accumulated_text.strip():
        output_file = os.path.join(output_dir, f"{os.path.basename(file_path).split('.')[0]}_part_{file_count}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(accumulated_text)


def batch_process(input_dir, output_dir, max_chars=950):
    # 遍历输入目录的所有文件和子目录
    for root, _, files in os.walk(input_dir):  # 使用 os.walk 递归遍历目录
        for file_name in files:
            # 只处理 .txt 和 .lrc 文件
            if file_name.endswith(('.txt', '.lrc')):  # 筛选符合条件的文件
                file_path = os.path.join(root, file_name)  # 获取文件的完整路径
                # 计算输出目录的子路径，以保持子目录结构
                relative_path = os.path.relpath(root, input_dir)  # 计算相对路径
                output_subdir = os.path.join(output_dir, relative_path)  # 目标输出子目录

                # 确保输出子目录存在
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                print(f"正在处理 {file_path}...")  # 打印当前处理的文件路径
                split_story(file_path, output_subdir, max_chars)  # 调用分割函数
                print(f"{file_name} 处理完成。")  # 打印处理完成提示


if __name__ == "__main__":
    # 指定包含 .txt 和 .lrc 文件的输入目录
    input_directory = "../../tempbak/[01]_1st:3生成:转音频<Speak>"  # 替换为你的输入目录路径
    # 指定用于保存分割后文件的输出目录
    output_directory = "../../tempbak/[02]_1st:5生成:切割字符[1000内][ 1st处理完毕 ]"  # 替换为你想要保存输出文件的目录路径

    batch_process(input_directory, output_directory)  # 批量处理输入目录中的文件