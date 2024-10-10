import os
import re

def process_text(input_text):
    lines = input_text.splitlines()
    output_lines = []

    for i, line in enumerate(lines):
        # 去除每行中的 <break> 标签
        line = re.sub(r'<break time="[^"]*"/>', '\n', line).strip()

        # 如果是空行，则在前一行添加 <br> 标签
        if line == '' and i > 0 and output_lines:
            output_lines[-1] += '@@@\n'
        else:
            output_lines.append(line)

    # 连接处理后的行
    return '\n'.join(output_lines)

def process_files(input_folder, output_folder):
    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # 只处理 .txt 文件
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 读取文件内容
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 处理文件内容
            processed_content = process_text(content)

            # 将处理后的内容写入到输出文件夹中的新文件
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(processed_content)

            print(f"Processed file: {filename}")

if __name__ == "__main__":
    # 设置输入文件夹和输出文件夹路径
    input_folder = '../../tempbak/[01]_1st:3生成:转音频<Speak>'
    output_folder ='../../tempbak/[04]_2nt:4生成:换行加@@@[手动ArcTime]'
    # 处理文件
    process_files(input_folder, output_folder)

    print("所有文件处理完成。")