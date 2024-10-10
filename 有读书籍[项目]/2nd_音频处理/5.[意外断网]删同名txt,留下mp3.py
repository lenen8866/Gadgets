import os

def delete_txt_with_same_name_as_mp3(directory):
    # 获取目录中所有文件
    files = os.listdir(directory)
    
    # 查找MP3文件和TXT文件
    mp3_files = [f for f in files if f.endswith('.mp3')]
    txt_files = [f for f in files if f.endswith('.txt')]
    
    # 对比MP3文件和TXT文件
    for mp3_file in mp3_files:
        # 获取MP3文件名（不含后缀）
        base_name = os.path.splitext(mp3_file)[0]
        # 构建同名的TXT文件名
        txt_file = base_name + '.txt'
        # 检查TXT文件是否存在
        if txt_file in txt_files:
            # 构建完整路径
            txt_path = os.path.join(directory, txt_file)
            # 删除同名的TXT文件
            os.remove(txt_path)
            print(f"Deleted: {txt_path}")

if __name__ == "__main__":
    # 指定要处理的目录
    directory = '/Users/jianxinwei/Pycharm/工具/temp/2nd:处理(1st:5生成文件)'
    delete_txt_with_same_name_as_mp3(directory)