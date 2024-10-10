import os
import glob
import re
from bs4 import BeautifulSoup, FeatureNotFound

def convert_to_span_format(input_file, output_directory):
    # 确保输出目录存在
    try:
        os.makedirs(output_directory, exist_ok=True)
    except Exception as e:
        print(f"创建输出目录时出错：{e}")
        return

    # 生成输出文件路径
    output_file = os.path.join(
        output_directory,
        os.path.splitext(os.path.basename(input_file))[0] + '.html'
    )

    with open(input_file, 'r', encoding='utf-8') as infile:
        first_char = infile.read(1)
        # 检查BOM字符
        if first_char == '\ufeff':
            print(f"检测到BOM字符，已跳过: {input_file}")
        else:
            infile.seek(0)

        entries = []
        current_entry = None

        # 正则表达式匹配 [时间] 文本
        pattern = re.compile(r'\[(\d+(\.\d+)?)\](.*)')

        for line in infile:
            line = line.strip()
            if not line:
                continue  # 跳过空行
            print(f"读取行: {line}")  # 打印读取的每一行
            match = pattern.match(line)
            if match:
                time_str = match.group(1)
                text = match.group(3).strip()

                try:
                    time = float(time_str)
                except ValueError:
                    print(f"无法转换时间戳: {time_str}")
                    continue

                if text:
                    # 如果有前一个字幕，设置其结束时间为当前时间
                    if current_entry:
                        current_entry['end'] = time

                    # 创建新的字幕条目
                    current_entry = {'start': time, 'end': None, 'text': text}
                    entries.append(current_entry)
                else:
                    # 只有时间戳，没有文本，通常表示下一个字幕的开始时间
                    if current_entry and current_entry['end'] is None:
                        current_entry['end'] = time

        # 为最后一个字幕条目设置结束时间（默认增加2秒）
        if entries and entries[-1]['end'] is None:
            entries[-1]['end'] = entries[-1]['start'] + 2.0  # 默认持续2秒

    # 使用 BeautifulSoup 生成 HTML
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write('<div class="content">\n')
            outfile.write('<p id="introText">\n')

            for entry in entries:
                start_time = entry['start']
                end_time = entry['end']
                text = entry['text']

                # # 移除特殊字符，如 "@@@"
                # text = text.replace('@@@', '').strip()

                # 判断是英文还是其他语言
                if any(ord(c) < 128 for c in text):  # 简单判断是否有ASCII字符
                    span_class = 'english'
                else:
                    span_class = 'saml'

                span = f'    <span class="{span_class}" data-start="{start_time:.2f}" data-end="{end_time:.2f}">{text}</span>\n'
                outfile.write(span)

            outfile.write('</p>\n')
            outfile.write('</div>\n')

        print(f"属性顺序已调整并保存到 '{output_file}'")

    except FeatureNotFound:
        print("错误: 'lxml' 解析器未找到，请确保已安装 'lxml'。")
        return

def batch_process_files(input_directory, output_directory):
    # 获取所有 .lrc 文件
    input_files = glob.glob(os.path.join(input_directory, '*.lrc'))

    if not input_files:
        print(f"在目录 '{input_directory}' 中没有找到任何 .lrc 文件。")
        return

    for input_file in input_files:
        print(f"处理文件: {input_file}")
        convert_to_span_format(input_file, output_directory)
        print(f"已处理文件: {input_file}")

if __name__ == "__main__":
    # 替换为您的输入和输出目录路径

    input_directory = '../../tempbak/[05_3rd分钟转秒'  # 输入文件夹路径
    output_directory = '../../tempbak/[06_4th:1生成,加入了parts:'  # 输出文件夹路径
    batch_process_files(input_directory, output_directory)
    print("所有文件处理完毕。")

