import os


def remove_empty_lines_and_first_line(text):
    """去掉文本中的空行和包含关键词 'Story' 的第一行"""
    lines = text.splitlines()

    # 检查第一行是否包含关键词 'Story'
    if lines and "Story" in lines[0]:
        cleaned_lines = [line for line in lines[1:] if line.strip()]  # 删除第一行并去掉空行
    else:
        cleaned_lines = [line for line in lines if line.strip()]  # 只去掉空行

    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text


def process_file(input_file, output_file):
    """处理单个文件，去掉空行和包含关键词 'Story' 的第一行并保存到新文件"""
    with open(input_file, 'r', encoding='utf-8') as infile:
        text_content = infile.read()

    # 去掉空行和包含关键词 'Story' 的第一行
    cleaned_text = remove_empty_lines_and_first_line(text_content)

    # 将处理后的内容保存到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(cleaned_text)


def process_files_in_directory(input_dir, output_dir):
    """批量处理目录中的文件"""
    # 检查输出目录是否存在，不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        # 只处理 .txt 文件
        if filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)  # 输出文件使用相同的文件名

            print(f"正在处理文件: {input_file}")
            process_file(input_file, output_file)
            print(f"文件处理完成并保存到: {output_file}")


input_directory = '/Users/jianxinwei/Desktop/临时/temp/7生成:LRC[拿这个打时间轴]/'  # 输入文件夹路径
output_directory = '../temp/8生成:LRC[finish]可以合并html了/'  # 输出文件夹路径

# 批量处理目录中的文件
process_files_in_directory(input_directory, output_directory)

print(f"所有文件处理完毕，结果已保存到目录: {output_directory}")