import os
import glob
from pydub import AudioSegment


def merge_audio_files(input_directory, output_directory):
    # 用于存储每个章节前缀对应的音频文件
    chapters = {}

    # 查找输入目录中的所有 mp3 文件
    audio_files = glob.glob(os.path.join(input_directory, "*.mp3"))

    # 将文件归类到章节，提取相同前缀
    for audio_file in audio_files:
        filename = os.path.basename(audio_file)
        chapter_prefix = "_part_".join(filename.split("_part_")[:-1])

        if chapter_prefix not in chapters:
            chapters[chapter_prefix] = []
        chapters[chapter_prefix].append(audio_file)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 合并每个章节的音频文件
    for chapter_prefix, files in chapters.items():
        files.sort()
        try:
            # 尝试读取第一个音频文件
            combined_audio = AudioSegment.from_file(files[0], format="mp3")

            # 逐个合并其他音频文件
            for audio_file in files[1:]:
                try:
                    next_audio = AudioSegment.from_file(audio_file, format="mp3")
                    combined_audio += next_audio
                except Exception as e:
                    print(f"警告：无法处理文件 {audio_file}，错误：{e}")
                    continue

            # 导出合并后的音频文件到指定的输出目录
            output_filename = f"{chapter_prefix}.mp3"
            output_path = os.path.join(output_directory, output_filename)
            combined_audio.export(output_path, format="mp3")
            print(f"合并完成: {output_filename}")

        except Exception as e:
            print(f"错误：无法处理章节 {chapter_prefix}，错误：{e}")


if __name__ == "__main__":
    # 指定包含要合并音频文件的输入目录

    input_directory = "../../tempbak//[02]_1st:5生成:切割字符[1000内][ 1st处理完毕 ]"  # 替换为你的音频文件所在目录
    # 指定用于保存合并后的音频文件的输出目录
    output_directory = "../../tempbak/[03]_2nd:2生成:完整音频mp3[放Lrc文件]"   # 替换为你想要保存输出文件的目录路径

    merge_audio_files(input_directory, output_directory)  # 开始合并音频文件