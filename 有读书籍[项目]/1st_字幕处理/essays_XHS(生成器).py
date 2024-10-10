import os
import re
import html
from essays_XHS import essays  # 确保 essays_data 已正确导入


# 把单词加粗,遍历一次
def bold_keywords_in_text(text, word_list):
    """在段落中找到关键词并加粗显示，支持中英文，大小写不敏感"""
    # 先转义 HTML 特殊字符
    text = html.escape(text)

    # 按关键词长度排序，先替换较长的关键词，避免短关键词干扰
    sorted_word_list = sorted(word_list, key=lambda x: len(x[0]), reverse=True)

    for word, _, word_cn in sorted_word_list:
        # 匹配英语单词的单复数形式（仅加粗，不改变原文）
        word_variants = [
            rf'(\b{re.escape(word)}s?\b)',  # 匹配单数和复数形式 (如: angel, angels)
            rf'(\b{re.escape(word)}es?\b)',  # 处理以 "es" 结尾的单词
            rf'(\b{re.escape(word)}ed\b)',  # 处理过去式形式
            rf'(\b{re.escape(word)}ing\b)'  # 处理进行时形式
        ]

        # 用正则匹配并加粗英文单词，保持原词形式不变
        for variant in word_variants:
            text = re.sub(variant, r'<strong>\1</strong>', text, flags=re.IGNORECASE)

        # 用正则匹配并加粗中文单词
        text = re.sub(rf'({re.escape(word_cn)})', r'<strong>\1</strong>', text)

    return text


def create_html_file(title_en, title_cn, intro_text, word_list, translation,
                     file_name, base_audio_path):
    # 定义音频文件路径
    audio_file_path = f"{base_audio_path}/{title_en.replace(' ', '_')}.mp3"

    # 定义HTML模板
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{title_en}</title>
    <link rel="stylesheet" href="/start/css/index.css">
    <script src="/start/js/script.js" defer></script>
</head>
<body>
<div class="container">
    <div class="header">
        <h2>{title_en}<br/>{title_cn}</h2>


    </div>


    <!-- 内容部分 -->
    <div class="content">
        <p id="introText">
            {"".join([f'<span class="english">{para}</span><br>' for para in intro_text])}
        </p>
    </div>


    <!-- 词汇学习部分 -->
    <div class="vocabulary">
        <div class="highlight-box">Words to Learn(要学习词语)</div>
        <div class="vocabulary-list">
            {"".join([f'<div class="vocabulary-item"><strong>{word[0]}</strong> {word[1]} {word[2]}</div>' for word in word_list])}
        </div>
    </div>

    <!-- 底部一句话 -->
        <div class="vocabulary">
        <div class="highlight-box">温馨提示</div>
        <div class="translation-text">

             <p><span class="saml">{translation}</span></p>
        </div>
    </div>
    
    
    
      <!--悬浮-->
    <div class="fixed-footer no-print ">
        <div class="audio-controls-container">
            <div class="audio-and-speed">
                <audio id="audio" controls>
                    <source id="audioSource" src="../mp3/Story_1:_From_the_Beginning.mp3" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                <div class="speed-control-container">
                    <label for="speedControl" class="speed-label"></label>
                    <select id="speedControl" class="speed-control">
                        <option value="0.5">0.5x</option>
                        <option value="0.6">0.6x</option>
                        <option value="0.7" selected="selected">0.7x</option>
                        <option value="0.8">0.8x</option>
                        <option value="0.9">0.9x</option>
                        <option value="1">1x</option>
                        <option value="1.25">1.25x</option>
                        <option value="1.5">1.5x</option>
                        <option value="2">2x</option>
                    </select>
                </div>
            </div>
        </div>
        <div class="controls-container">
            <button onclick="skipBackward()" class="custom-button" id="backwardButton">后退3秒</button>
            <button onclick="togglePlayPause()" class="custom-button" id="playPauseButton">暂停</button>
            <button onclick="skipForward()" class="custom-button" id="forwardButton">前进3秒</button>
            <button id="toggleChineseButton">隐藏中文</button>
            <button id="copyEnglishButton">复制英文</button>
        </div>
    </div>

</div>
</body>
</html>
    """

    # 保存HTML文件
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_template)

    print(f"HTML 文件 '{file_name}' 已生成.")


# 批量生成文件
def generate_html_files_in_batches(base_dir, base_audio_path):
    total_files = len(essays)

    for i, essay in enumerate(essays):
        batch_start = (i // 50) * 50 + 1
        batch_end = min((i // 50 + 1) * 50, total_files)
        folder_name = f"{batch_start}-{batch_end}"

        target_dir = os.path.join(base_dir, folder_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        file_name = f"{target_dir}/{essay['title_en'].replace(' ', '_')}.html"

        create_html_file(
            essay['title_en'],
            essay['title_cn'],
            essay['intro_text'],
            essay['word_list'],
            essay['translation'],

            file_name,
            base_audio_path
        )


# 设置路径
target_directory = '/Users/jianxinwei/Desktop/临时/html/books/KWS/XiaoHongShu/list_html'
audio_directory = '../mp3'

# 调用生成HTML文件的批量生成函数
generate_html_files_in_batches(target_directory, audio_directory)
