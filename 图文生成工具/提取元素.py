import json
import os

# 加载 JSON 文件
with open('text_content.json', 'r', encoding='utf-8') as f:
    content_data = json.load(f)

# 创建输出文件夹
output_folder = 'output_texts'
os.makedirs(output_folder, exist_ok=True)

# 遍历每个字典的 `text_groups`，并为每个创建一个 .txt 文件
for entry in content_data:
    # 使用英文标题生成文件名
    title_en = entry["title"]["en"].replace(" ", "_")
    file_path = os.path.join(output_folder, f"{title_en}.txt")

    # 将 `text_groups` 中的内容写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        for text_group in entry["text_groups"]:
            # 写入英文部分并加上 <break time="4s"/>
            file.write(f"<break time=\"4s\"/>{text_group[0]} <break time=\"4s\"/>\n")

    print(f"已生成文件: {file_path}")