import json
import os
import random
from PIL import Image, ImageDraw, ImageFont

# 输入和输出文件夹路径
input_folder = "path/to/input_folder"  # 输入文件夹路径
output_folder = "path/to/output_folder"  # 输出文件夹路径
os.makedirs(output_folder, exist_ok=True)  # 创建输出文件夹（若不存在）

# 控制是否添加标题：1 为添加标题，0 为不添加标题
add_title = 0

# 设置字体大小和颜色
title_font_size_en = 48  # 英文标题字体大小
title_font_size_cn = 42  # 中文标题字体大小（稍小）
font_size_en = 40  # 英文字体大小
font_size_cn = 36  # 中文字体大小
font_size_phonetic = 32  # 音标字体大小
font_color = (255, 255, 255)  # 正文字颜色，白色
title_color = (255, 215, 0)  # 标题颜色，金色
outline_color = (0, 0, 0)  # 轮廓颜色，黑色
mask_opacity = 128  # 蒙版透明度

# 加载字体
try:
    font_path = "/System/Library/Fonts/Arial Unicode.ttf"  # 替换为支持 Unicode 的字体路径
    title_font_en = ImageFont.truetype(font_path, title_font_size_en)  # 英文标题字体
    title_font_cn = ImageFont.truetype(font_path, title_font_size_cn)  # 中文标题字体
    font_en = ImageFont.truetype(font_path, font_size_en)  # 英文字体
    font_cn = ImageFont.truetype(font_path, font_size_cn)  # 中文字体
    font_phonetic = ImageFont.truetype(font_path, font_size_phonetic)  # 音标字体
except IOError:
    print("指定的 Unicode 字体文件未找到或不可用，请确认字体路径或使用支持 Unicode 的字体。")
    exit(1)

# 从 JSON 文件中读取文本内容
with open('text_content.json', 'r', encoding='utf-8') as f:
    content_data = json.load(f)

# 从输入文件夹中随机选择一张图片
files = [f for f in os.listdir(input_folder) if f.endswith((".jpg", ".png", ".jpeg"))]
if not files:
    print("输入文件夹中没有找到有效的图片文件。")
    exit(1)

# 绘制文字带轮廓的函数
def draw_text_with_outline(draw, position, text, font, fill, outline_fill, outline_width=2):
    x, y = position
    # 绘制轮廓
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_fill)
    # 绘制文字
    draw.text((x, y), text, font=font, fill=fill)

# 处理每组内容并生成图片
for index, data in enumerate(content_data):
    title_text_en = data["title"]["en"] if add_title == 1 else ""
    title_text_cn = data["title"]["cn"] if add_title == 1 else ""
    text_groups = data["text_groups"]

    filename = random.choice(files)  # 随机选择一张背景图片
    img_path = os.path.join(input_folder, filename)
    img = Image.open(img_path).convert("RGBA")

    # 创建一个半透明蒙版层
    mask_layer = Image.new("RGBA", img.size, (0, 0, 0, mask_opacity))
    img = Image.alpha_composite(img, mask_layer)

    # 创建透明文字层
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # 计算内容总高度
    total_text_height = 0
    line_spacing = 12  # 行间距
    group_spacing = 50  # 每组之间的间距

    # 如果有标题，计算标题高度
    if add_title == 1:
        title_width_en, title_height_en = draw.textsize(title_text_en, font=title_font_en)
        title_width_cn, title_height_cn = draw.textsize(title_text_cn, font=title_font_cn)
        total_text_height += title_height_en + title_height_cn + 30  # 英文和中文标题的高度加上间距

    # 累加每组内容的高度
    for en_text, cn_text, phonetic in text_groups:
        text_width_en, text_height_en = draw.textsize(en_text, font=font_en)
        text_width_phonetic, text_height_phonetic = draw.textsize(phonetic, font=font_phonetic)
        text_width_cn, text_height_cn = draw.textsize(cn_text, font=font_cn)
        total_text_height += text_height_en + text_height_phonetic + text_height_cn + group_spacing

    # 设置垂直居中的起始Y坐标
    start_y = (img.height - total_text_height) / 2

    # 绘制标题（如果 `add_title` 为 1）
    if add_title == 1:
        title_x_en = (img.width - title_width_en) / 2
        draw_text_with_outline(draw, (title_x_en, start_y), title_text_en, title_font_en, title_color, outline_color)

        title_x_cn = (img.width - title_width_cn) / 2
        draw_text_with_outline(draw, (title_x_cn, start_y + title_height_en + 10), title_text_cn, title_font_cn,
                               title_color, outline_color)

        # 更新Y坐标为标题下方
        current_y = start_y + title_height_en + title_height_cn + 20 + group_spacing
    else:
        current_y = start_y

    # 绘制每组内容，英文在上，音标在中，中文在下
    for en_text, cn_text, phonetic in text_groups:
        text_width_en, text_height_en = draw.textsize(en_text, font=font_en)
        text_width_phonetic, text_height_phonetic = draw.textsize(phonetic, font=font_phonetic)
        text_width_cn, text_height_cn = draw.textsize(cn_text, font=font_cn)

        # 计算每行的X坐标，使其水平居中
        text_position_x_en = (img.width - text_width_en) / 2
        text_position_x_phonetic = (img.width - text_width_phonetic) / 2
        text_position_x_cn = (img.width - text_width_cn) / 2

        # 绘制英文文字
        draw_text_with_outline(draw, (text_position_x_en, current_y), en_text, font_en, font_color, outline_color)

        # 绘制音标文字，位置在英文文字下方
        draw_text_with_outline(draw, (text_position_x_phonetic, current_y + text_height_en + line_spacing), phonetic,
                               font_phonetic, font_color, outline_color)

        # 绘制中文文字，位置在音标文字下方
        draw_text_with_outline(draw, (
        text_position_x_cn, current_y + text_height_en + text_height_phonetic + 2 * line_spacing), cn_text, font_cn,
                               font_color, outline_color)

        # 更新Y坐标为下一组内容留出间距
        current_y += text_height_en + text_height_phonetic + text_height_cn + group_spacing

    # 将文字层与已添加蒙版的图片叠加
    combined = Image.alpha_composite(img, txt_layer).convert("RGB")

    # 保存处理后的图片到输出文件夹，以图片序号命名
    output_path = os.path.join(output_folder, f"output_{index}.png")
    combined.save(output_path, format="PNG")  # 保存为 PNG 格式

    print(f"已处理并保存文件：{output_path}")