import os

def add_br_tags_to_empty_lines(text):
    """在文本中的空行上方和下方各添加 <br> 标签"""
    lines = text.splitlines()  # 将文本按行分割
    result_lines = []  # 用于存储处理后的行

    for i, line in enumerate(lines):
        # 处理当前行是 <speak> 标签的情况
        if line.strip() == "<speak>":
            result_lines.append(line)  # 直接添加 <speak> 标签
            continue

        if line.strip() == "":
            # 仅在下一行不是空行的情况下添加 <br> 标签
            if i < len(lines) - 1 and lines[i + 1].strip() != "":
                # 只有当下一行不为空时，才添加 <br> 标签
                if result_lines and result_lines[-1] != "@@@":
                    result_lines[-1] += "@@@\n"  # 将 <br> 标签附加到上一行
        else:
            result_lines.append(line)  # 添加当前行

    # 将处理后的行重新合并为文本
    return "\n".join(result_lines)

# 批量处理文件
input_directory = '../temp/6生成:源LRC'  # 输入文件夹路径
output_directory = '../temp/7生成:LRC[拿这个打时间轴]/'  # 输出文件夹路径

# 确保输出目录存在
os.makedirs(output_directory, exist_ok=True)

# 遍历输入目录中的所有文件
for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):  # 只处理文本文件
        input_file_path = os.path.join(input_directory, filename)

        # 读取输入文件内容
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()

        # 处理文本
        output_text = add_br_tags_to_empty_lines(input_text)

        # 写入输出文件
        output_file_path = os.path.join(output_directory, filename)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text)

print("批量处理完成！")