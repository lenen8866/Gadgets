import os
import moviepy.editor as mp
import ffmpeg
from glob import glob
import pysrt

def generate_centered_ass(srt_file, ass_file, center_margin=10, line_spacing=10):
    """
    从 SRT 字幕文件生成带高亮、淡化效果的 ASS 字幕文件：
    当前行高亮，已读行淡化，未读行浅灰。

    参数：
        srt_file (str): 输入的 SRT 字幕文件路径。
        ass_file (str): 输出的 ASS 字幕文件路径。
        center_margin (int): 当前行字幕在屏幕中央的垂直位置。
        line_spacing (int): 每行之间的垂直间距。
    """
    subs = pysrt.open(srt_file)
    with open(ass_file, 'w', encoding='utf-8') as f:
        # 写入 ASS 文件头部信息
        f.write(
            '[Script Info]\nTitle: Highlighted Scrolling Lyrics\nScriptType: v4.00+\nCollisions: Normal\nPlayDepth: 0\n\n'
        )

        # 定义字幕样式
        f.write('[V4+ Styles]\n')
        f.write('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, '
                'Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, '
                'MarginL, MarginR, MarginV, Encoding\n')

        # 当前行样式：绿色字体，字体较大
        f.write(
            'Style: CurrentLine,Arial,40,&H0000FF00,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,{center_margin},1\n'
        )
        # 已读行样式：浅灰色字体
        f.write(
            'Style: ReadLine,Arial,36,&H00777777,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,{center_margin},1\n'
        )
        # 未读行样式：更浅的灰色字体
        f.write(
            'Style: UnreadLine,Arial,36,&H00AAAAAA,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,{center_margin},1\n'
        )

        f.write('[Events]\n')
        f.write('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')

        # 写入字幕内容
        for i, sub in enumerate(subs):
            start_time = "{:02}:{:02}:{:02}.{:02}".format(
                sub.start.hours, sub.start.minutes, sub.start.seconds, int(sub.start.milliseconds / 10)
            )
            end_time = "{:02}:{:02}:{:02}.{:02}".format(
                sub.end.hours, sub.end.minutes, sub.end.seconds, int(sub.end.milliseconds / 10)
            )
            text = sub.text.replace('\n', ' ')

            # 设置不同位置和样式
            if i == 0:
                style = "CurrentLine"  # 当前行高亮显示
                margin_v = center_margin  # 当前行固定在中间
            elif i < len(subs) // 2:
                style = "ReadLine"
                margin_v = center_margin - (len(subs) // 2 - i) * line_spacing  # 已读行向上滚动并淡化
            else:
                style = "UnreadLine"
                margin_v = center_margin + (i - len(subs) // 2) * line_spacing  # 未读行在下方等待

            # 写入每行字幕的对话部分
            f.write("Dialogue: 0,{},{},{},,0,0,{},,{}\n".format(start_time, end_time, style, margin_v, text))


# 合成视频并添加字幕
def create_video_with_audio_and_subtitles(audio_file, image_file, subtitle_file, output_file, resolution=(1280, 720)):
    print(f"处理文件：{audio_file}")
    print(f"背景图片：{image_file}")
    print(f"字幕文件：{subtitle_file}")

    # 检查音频、图片和字幕文件是否存在
    if not os.path.exists(audio_file):
        print(f"音频文件不存在：{audio_file}")
        return
    if not os.path.exists(image_file):
        print(f"背景图片不存在：{image_file}")
        return
    if not os.path.exists(subtitle_file):
        print(f"字幕文件不存在：{subtitle_file}")
        return

    try:
        # 加载背景图片并调整大小
        image_clip = mp.ImageClip(image_file).set_duration(mp.AudioFileClip(audio_file).duration)
        image_clip = image_clip.resize(newsize=resolution)
        audio_clip = mp.AudioFileClip(audio_file)
        video_clip = image_clip.set_audio(audio_clip)

        # 保存临时视频文件（不带字幕）
        temp_video = "temp_video.mp4"
        video_clip.write_videofile(temp_video, codec="libx264", fps=24, verbose=False, logger=None)

        # 添加 ASS 字幕到视频中
        add_subtitles(temp_video, subtitle_file, output_file)
        os.remove(temp_video)  # 删除临时视频文件
        print(f"完成合成：{output_file}")
    except Exception as e:
        print(f"处理文件 {audio_file} 时出错: {e}")


# 使用 ffmpeg 添加字幕到视频
def add_subtitles(video_file, subtitle_file, output_file):
    try:
        ffmpeg.input(video_file).output(
            output_file,
            vf=f"ass='{subtitle_file}'"
        ).run(overwrite_output=True)
    except Exception as e:
        print(f"添加字幕时出错: {e}")


# 批量处理函数
def batch_process(audio_folder, subtitle_folder, image_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取所有音频文件
    audio_files = glob(os.path.join(audio_folder, "*.mp3"))
    for audio_file in audio_files:
        base_name = os.path.splitext(os.path.basename(audio_file))[0]

        # 生成 ASS 文件
        ass_file = os.path.join(subtitle_folder, f"{base_name}.ass")
        srt_file = os.path.join(subtitle_folder, f"{base_name}.srt")

        if os.path.exists(srt_file):
            print(f"生成高亮 ASS 文件：{ass_file}")
            generate_centered_ass(srt_file, ass_file)

        if os.path.exists(ass_file):
            output_file = os.path.join(output_folder, f"{base_name}_output.mp4")
            print(f"正在处理：{audio_file} 和 {ass_file}")
            create_video_with_audio_and_subtitles(audio_file, image_file, ass_file, output_file)
        else:
            print(f"未找到字幕文件：{ass_file}，跳过 {audio_file}")


# 设置文件夹路径
audio_folder = "/Users/jianxinwei/Desktop/q"
subtitle_folder = "/Users/jianxinwei/Desktop/q"
image_file = "/Users/jianxinwei/Desktop/cozy_reading_nook.jpg"
output_folder = "/Users/jianxinwei/Desktop/q/output_videos"

# 批量处理
batch_process(audio_folder, subtitle_folder, image_file, output_folder)
print("所有文件处理完成！")