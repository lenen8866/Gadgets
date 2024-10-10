import os

def insert_break_in_files(directory):
    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # 检查是否是文件（而不是目录）
        if os.path.isfile(file_path):
            with open(file_path, 'r+', encoding='utf-8') as file:
                content = file.readlines()
                # 在第一行插入 <break time="3s"/>
                content.insert(0, '<break time="0.5s"/>')
                # 将文件指针移到文件开头
                file.seek(0)
                # 将修改后的内容写回文件
                file.writelines(content)
            print(f"已在 {filename} 中插入 break")

# 将 'your_directory' 替换为包含文件的目录路径
insert_break_in_files('../../tempbak/[01]_1st:3生成:转音频<Speak>')