import os
import glob

def replace_keywords_in_file(input_file, output_directory):
    output_file = os.path.join(output_directory, os.path.basename(input_file))  # 输出文件路径，保留文件名

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 替换指定的字符串
            modified_line = line.replace('@@@</span>', '</span><br>\n')
            outfile.write(modified_line)  # 写入修改后的行

    print(f"文件 {input_file} 中的关键词已替换，并写入到 {output_file}。")

# 批量处理文件
def batch_process_files(input_directory, output_directory):
    # 创建输出目录（如果不存在的话）
    os.makedirs(output_directory, exist_ok=True)

    # 获取所有符合条件的 HTML 文件
    input_files = glob.glob(os.path.join(input_directory, '*.html'))  # 假设输入文件为 .html 格式

    if not input_files:
        print(f"在目录 '{input_directory}' 中没有找到任何 .html 文件。")
        return  # 如果没有找到文件，提前返回

    for input_file in input_files:
        print(f"处理文件: {input_file}")  # 打印当前处理的文件
        replace_keywords_in_file(input_file, output_directory)

# 使用示例
input_directory = '../../tempbak/[06_4th:1生成,加入了parts:'  # 输入文件夹路径
output_directory = '../../tempbak/[07:4th:2生成:span_to_br'  # 输出文件夹路径
batch_process_files(input_directory, output_directory)
print("所有文件处理完毕。")
