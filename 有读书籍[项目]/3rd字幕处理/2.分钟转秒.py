import os

# 转换时间格式为秒的函数
def convert_time_to_seconds(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 查找时间戳
            if line.startswith('[') and ']' in line:
                time_str = line[1:line.index(']')]
                text = line[line.index(']') + 1:].strip()  # 获取时间戳后的文本

                try:
                    # 解析时间（分钟和秒）
                    if ':' in time_str:
                        minutes, seconds = time_str.split(':')
                        # 将时间转换为秒
                        total_seconds = int(minutes) * 60 + float(seconds)
                    else:
                        # 没有分钟部分，只有秒
                        total_seconds = float(time_str)

                    # 对零秒特殊处理
                    if abs(total_seconds) < 1e-6:
                        new_time_str = "[0]"
                    else:
                        # 转换为秒，保留两位小数并去除多余的零
                        new_time_str = f"[{total_seconds:.2f}]".rstrip('0').rstrip('.')

                    # 替换行中的时间戳，并保留文本
                    new_line = f"{new_time_str}{' ' + text if text else ''}\n"
                    outfile.write(new_line)
                except ValueError as e:
                    print(f"解析时间出错: {time_str} 行: {line}")
                    outfile.write(line)
            else:
                # 直接写入没有时间戳的行
                outfile.write(line)

# 处理文件夹中所有的 .LRC 文件
def process_folder(input_folder, output_folder):
    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for file_name in os.listdir(input_folder):
        # 只处理 .LRC 文件
        if file_name.endswith('.lrc'):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, f"{file_name}")

            # 转换时间格式
            convert_time_to_seconds(input_file_path, output_file_path)
            print(f"已处理文件: {file_name}，输出到: {output_file_path}")

# 使用示例
input_folder = '../../tempbak/[03]_2nd:2生成:完整音频mp3[放Lrc文件]'  # 输入文件夹路径
output_folder = '../../tempbak/[05_3rd分钟转秒'  # 输出文件夹路径

process_folder(input_folder, output_folder)
print(f"所有文件已处理完毕，结果保存在 {output_folder} 中。")
