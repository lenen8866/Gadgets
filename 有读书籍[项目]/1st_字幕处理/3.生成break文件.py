# 早期的文件处理
import os
import re

# 第一步：使用 generate_breaks 函数处理文本，并保存中间结果
def generate_breaks(text):
    # 分段处理，每个自然段之间通过两个换行符分隔
    paragraphs = text.split('\n\n')  # 使用双换行符分割自然段

    result = []

    for paragraph in paragraphs:
        # 对每个自然段中的句子进行处理
        sentences = re.split(r'([.,])', paragraph)
        paragraph_result = []

        for i in range(0, len(sentences) - 1, 2):  # 遍历句子和标点符号
            sentence = sentences[i].strip()
            punctuation = sentences[i + 1]

            if sentence:
                # 计算句子中的单词数量
                words = sentence.split(' ')
                word_count = len(words)

                # 根据单词数量设置 break 时间
                if word_count == 1:
                    break_time = '0.5s'
                elif word_count == 2:
                    break_time = '1s'
                elif word_count == 3:
                    break_time = '1s'
                elif word_count == 4:
                    break_time = '1.3s'
                elif word_count == 5:
                    break_time = '1.8s'
                else:
                    break_time = '2s'

                # 生成带有 break 时间的句子
                formatted_sentence = f"{sentence}{punctuation}<break time=\"{break_time}\"/>"
                paragraph_result.append(formatted_sentence)

        # 将处理过的自然段加入结果
        result.append('\n'.join(paragraph_result))  # 保持段内的句子换行

    # 将处理过的自然段用双换行符拼接，保持自然段之间有空行
    output = '\n\n'.join(result)

    return output

# 第一阶段处理并生成中间文件，删除原始 .txt 文件
def process_text_files_in_directory(directory_path):
    """第一步：遍历目录中的所有 .txt 文件并应用 generate_breaks 处理"""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # 只处理 .txt 文件
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()

                # 对文本内容应用 generate_breaks 函数
                updated_text = generate_breaks(text_content)

                # 将处理后的内容保存到中间文件，并保持原有的换行格式
                output_file_path = file_path.replace('.txt', '_processed_stage1.txt')
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_text)

                print(f"第一步处理完成：{output_file_path}")

                # 删除原始的 .txt 文件
                try:
                    os.remove(file_path)
                    print(f"原始文件 {file_path} 已删除")
                except Exception as e:
                    print(f"删除原始文件 {file_path} 时出错: {e}")

# 第二步：使用 insert_break 函数进行进一步处理
def insert_break(sentence):
    # 分离出文本部分和结尾的<break time="x"/>部分
    match = re.match(r'(.*?)(<break time="[^"]*"/>)*$', sentence)
    if match:
        text = match.group(1)  # 纯文本部分
        break_tag = match.group(2) if match.group(2) else ''  # 保留原来的<break time="x"/>部分

        # 将句子分割为单词
        words = text.split(' ')

        # 如果单词超过6个, 在中间插入<break time="2s"/>
        if len(words) >= 6 :
            midpoint = len(words) // 2
            new_sentence = ' '.join(words[:midpoint]) + '<break time="2s"/> ' + ' '.join(words[midpoint:])
            return new_sentence + break_tag  # 加回结尾的break tag
        else:
            return sentence  # 如果不超过6个单词, 原样返回
    else:
        return sentence

# 处理单个文件
def process_file(input_file, output_file):
    try:
        # 打开中间处理的文件读取
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        # 逐行处理
        processed_lines = [insert_break(line.strip()) for line in lines]

        # 将处理后的内容写入最终文件
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for line in processed_lines:
                outfile.write(line + '\n')

    except Exception as e:
        print(f"处理文件时出错: {e}")

# 第二阶段：处理第一步生成的中间文件，并删除中间文件
def process_files_with_output_directory(input_dir, output_dir):
    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"输出目录 {output_dir} 不存在，已创建该目录。")

    # 遍历第一步生成的中间文件
    for filename in os.listdir(input_dir):
        # 只处理第一步生成的 _processed_stage1.txt 文件
        if filename.endswith('_processed_stage1.txt'):
            input_file = os.path.join(input_dir, filename)  # 输入文件路径
            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0].replace('_processed_stage1', '')}_final.txt")  # 生成最终处理后的文件名

            # 处理文件并保存到指定目录
            process_file(input_file, output_file)

            # 确保文件处理完成后再删除中间文件
            if os.path.exists(output_file):
                try:
                    print(f"准备删除中间文件: {input_file}")
                    os.remove(input_file)
                    print(f"中间文件: {input_file} 已删除")
                except Exception as e:
                    print(f"删除中间文件时出错: {e}")
            else:
                print(f"处理文件失败: {input_file}，未找到生成的 {output_file}")

# 执行两个步骤的函数
def execute_steps(input_directory, output_directory):
    print("第一步：应用 generate_breaks 处理")
    process_text_files_in_directory(input_directory)

    print("\n第二步：应用 insert_break 处理")
    process_files_with_output_directory(input_directory, output_directory)

# 示例用法：指定输入目录和输出目录

input_directory = "/Users/jianxinwei/Pycharm/书本朗读[英语]/holybible故事书/html/books/school/Growing_in_faith_and_charcter/list_html/1-48"
output_directory = "../../tempbak/[01]_1st:3生成:转音频<Speak>"  # 输出文件夹路径

# 执行第一步和第二步处理
execute_steps(input_directory, output_directory)

print(f"所有文件处理完毕，结果已保存到目录: {output_directory}")