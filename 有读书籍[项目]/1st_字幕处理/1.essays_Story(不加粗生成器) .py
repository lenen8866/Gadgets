import os
import html
from essays_Story import essays  # 确保 essays_data 已正确导入

# 创建 HTML 文件的函数，移除了 bold_keywords_in_text 函数的调用
def create_html_file(
    title_en, title_cn, intro_text, word_list, translation=None,
    poem_en=None, poem_cn=None, memory_gem_en=None, memory_gem_cn=None,
    file_name=None, base_audio_path=None):
    # 定义音频文件路径
    audio_file_path = f"{base_audio_path}/{title_en.replace(' ', '_')}.mp3"

    # 定义 HTML 模板
    html_template = f"""
    <!DOCTYPE html>
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
        <div id="nav-placeholder"></div>
        <div class="header">
            <h2>{title_en}<br/>{title_cn}</h2>
        </div>
            
        <div id="herder-placeholder"></div>
        
        
        <!-- 内容部分 -->
        <div class="content">
            <div id="header-placeholder"></div>
            <p id="introText">
                {"".join([
                    f'    <span class="english">{para}</span><br>'
                    f'    <span class="saml">{trans}</span><br>'
                    for para, trans in intro_text
                ])}
            </p>
        </div>

        {"<div class='vocabulary'><div class='highlight-box'>中文译文</div><div class='translation-text'><p>{translation}</p></div></div>" if translation else ""}

        {"<div class='vocabulary'><div class='highlight-box'>Learn the Poem(学习这首诗)</div><div class='poem-content'><p class='english'>{poem_en}</p><p><span class='saml'>{poem_cn}</span></p></div></div>" if poem_en or poem_cn else ""}

        <!-- 词汇学习部分 -->
        <div class="vocabulary">
            <div class="highlight-box">Words to Learn(要学习词语)</div>
            <div class="vocabulary-list">
                {"".join([
                    f'<div class="vocabulary-item">{word[0]} {word[1]} {word[2]}</div>'
                    for word in word_list
                ])}
            </div>
        </div>

        <!-- 底部 - 圣经一句话 -->
        {"<div class='vocabulary'><div class='highlight-box'>Memory Gem</div>" + 
            (f"<div class='translation-text'><p class='english'>{memory_gem_en}</p></div>" if memory_gem_en else "") +
            (f"<div class='translation-text'><p class='saml'>{memory_gem_cn}</p></div>" if memory_gem_cn else "") +
        "</div>" if memory_gem_en or memory_gem_cn else ""}
        <div id="footer-placeholder"></div>
        
        
        
        
            <!--悬浮-->
    <div class="fixed-footer no-print">
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

    # 保存 HTML 文件
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(html_template)
        print(f"HTML 文件 '{file_name}' 已生成.")
    except Exception as e:
        print(f"生成 HTML 文件时出错: {e}")

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

        # 使用 dict.get() 获取字段，如果字段缺失则返回 None
        create_html_file(
            essay['title_en'],
            essay['title_cn'],
            essay['intro_text'],
            essay['word_list'],
            essay.get('translation'),
            essay.get('poem_en'),
            essay.get('poem_cn'),
            essay.get('memory_gem_en'),
            essay.get('memory_gem_cn'),
            file_name,
            base_audio_path
        )

# 调用批量生成函数
target_directory = "/Users/jianxinwei/Github/text/books_mate/holybible故事书/html/books/school/Growing_in_faith_and_charcter/list_html"
audio_directory = '../mp3'
generate_html_files_in_batches(target_directory, audio_directory)