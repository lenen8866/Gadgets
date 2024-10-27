import os
import moviepy.editor as mp
import ffmpeg
from glob import glob

def create_video_with_audio_and_subtitles(audio_file, background_file, subtitle_file, output_file, resolution=(1280, 720)):
    print(f"处理文件：{audio_file}")
    print(f"背景文件：{background_file}")
    print(f"字幕文件：{subtitle_file}")

    # 检查文件存在
    if not os.path.exists(audio_file):
        print(f"音频文件不存在：{audio_file}")
        return
    if not os.path.exists(background_file):
        print(f"背景文件不存在：{background_file}")
        return
    if not os.path.exists(subtitle_file):
        print(f"字幕文件不存在：{subtitle_file}")
        return

    try:
        # 判断背景文件类型，图片或视频
        if background_file.lower().endswith(('.mp4', '.mov', '.avi')):
            # 如果是视频
            background_clip = mp.VideoFileClip(background_file).resize(newsize=resolution)
            background_clip = background_clip.set_duration(mp.AudioFileClip(audio_file).duration)
        else:
            # 如果是图片
            background_clip = mp.ImageClip(background_file).set_duration(mp.AudioFileClip(audio_file).duration)
            background_clip = background_clip.resize(newsize=resolution)

        # 加载音频并合成视频
        audio_clip = mp.AudioFileClip(audio_file)
        video_clip = background_clip.set_audio(audio_clip)

        # 保存临时无字幕视频
        temp_video = "temp_video.mp4"
        video_clip.write_videofile(temp_video, codec="libx264", fps=24, verbose=False, logger=None)

        # 添加字幕并清理
        add_subtitles(temp_video, subtitle_file, output_file)
        os.remove(temp_video)
        print(f"完成合成：{output_file}")
    except Exception as e:
        print(f"处理文件 {audio_file} 时出错: {e}")

def add_subtitles(video_file, subtitle_file, output_file):
    # 使用 FFmpeg 添加字幕
    try:
        ffmpeg.input(video_file).output(
            output_file,
            vf=f"subtitles={subtitle_file}:force_style='FontSize=24,PrimaryColour=&HFFFFFF&'"
        ).run(overwrite_output=True)
    except Exception as e:
        print(f"添加字幕时出错: {e}")

def batch_process(audio_folder, subtitle_folder, background_file, output_folder):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取所有音频文件
    audio_files = glob(os.path.join(audio_folder, "*.mp3"))
    for audio_file in audio_files:
        # 找到对应的字幕文件
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        subtitle_file = os.path.join(subtitle_folder, f"{base_name}.srt")

        if os.path.exists(subtitle_file):
            output_file = os.path.join(output_folder, f"{base_name}_out.mp4")
            print(f"正在处理：{audio_file} 和 {subtitle_file}")
            create_video_with_audio_and_subtitles(audio_file, background_file, subtitle_file, output_file)
        else:
            print(f"未找到字幕文件：{subtitle_file}，跳过 {audio_file}")

# 配置文件夹路径
audio_folder = "/Users/jianxinwei/Desktop/mp3"
subtitle_folder = "/Users/jianxinwei/Desktop/mp3"
background_file = "/Users/jianxinwei/Desktop/cozy_reading_nook.jpg"  # 可以是图片或视频文件
output_folder = "/Users/jianxinwei/Desktop/mp3/output_videos"

# 批量处理
batch_process(audio_folder, subtitle_folder, background_file, output_folder)
print("所有文件处理完成！")