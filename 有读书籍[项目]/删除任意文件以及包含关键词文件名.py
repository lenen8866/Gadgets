import os

def delete_txt_files_with_processed(directory):
    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 说明endswith(""),删除没有尾缀的文件
            #可以设置任何的尾缀的文件file.endswith("txt"),("html"),
            #而“_processed”是属于关键词,文件名的关键词,可以随意改要删除的.
            if file.endswith("txt") and "" in file:  # 检查.txt文件名中是否包含"_processed"
                file_path = os.path.join(root, file)
                print(f"Deleting file: {file_path}")
                os.remove(file_path)

if __name__ == "__main__":
    # 在这里指定你想要扫描的目录
    directory = "/Users/jianxinwei/Desktop/临时/转音频<Speak>文件"  # 替换为你的实际目录路径
    delete_txt_files_with_processed(directory)