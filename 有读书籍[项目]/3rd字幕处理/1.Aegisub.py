import os
import speech_recognition as sr
from pydub import AudioSegment


def transcribe_audio_to_lrc(audio_file, segments, output_file):
    recognizer = sr.Recognizer()
    # 加载 mp3 文件
    audio = AudioSegment.from_mp3(audio_file)

    # 准备 lrc 输出格式的列表
    lrc_output = []

    # 获取音频的时长（毫秒）
    duration = len(audio)

    # 假设文本分布均匀，按比例分割音频
    total_text_length = sum(len(segment) for segment in segments)

    start_time_ms = 0

    # 计算每句对应的音频时长（假设每句的时长与其长度成正比）
    first_line = True  # 标记第一行

    for segment in segments:
        segment_lines = segment.strip().split("\n")  # 按每行分割文本

        for line in segment_lines:
            line = line.strip()
            if not line:  # 如果是空行，跳过
                continue

            # 根据文本长度的比例，计算每行文本的时长
            line_duration = int((len(line) / total_text_length) * duration)

            # 从音频中提取当前片段
            audio_chunk = audio[start_time_ms:start_time_ms + line_duration]

            # 暂存音频片段到临时文件
            temp_wav_file = "Aegisub/temp_segment.wav"
            audio_chunk.export(temp_wav_file, format="wav")

            # 识别当前音频片段中的文本
            with sr.AudioFile(temp_wav_file) as source:
                audio_data = recognizer.record(source)
                try:
                    # 获取时间戳
                    minutes = start_time_ms // 60000
                    seconds = (start_time_ms % 60000) / 1000

                    # 格式化时间戳
                    timestamp = f"[{int(minutes):02}:{seconds:05.2f}]"

                    # 只从第二行开始添加空时间戳行
                    if not first_line:
                        lrc_output.append(f"{timestamp} ")

                    # 添加时间戳行和文本行
                    lrc_output.append(f"{timestamp}{line}")
                    # 更新开始时间
                    start_time_ms += line_duration

                    # 标记第一行已处理
                    first_line = False

                except sr.UnknownValueError:
                    print(f"无法识别音频内容: {audio_file}")
                except sr.RequestError as e:
                    print(f"请求结果出错：{e}")

    # 添加最后的结束时间戳
    minutes = start_time_ms // 60000
    seconds = (start_time_ms % 60000) / 1000
    end_timestamp = f"[{int(minutes):02}:{seconds:05.2f}] "
    lrc_output.append(end_timestamp)

    # 保存 .lrc 文件
    with open(output_file, "w") as f:
        for line in lrc_output:
            f.write(line + "\n")

    print(f"LRC 文件已生成：{output_file}")


def batch_process_lrc(audio_directory, text_directory, output_directory):
    # 遍历音频文件目录
    for file in os.listdir(audio_directory):
        if file.endswith(".mp3"):
            # 音频文件路径
            audio_file = os.path.join(audio_directory, file)
            # 对应的文本文件路径
            txt_file = os.path.join(text_directory, os.path.splitext(file)[0] + ".txt")

            if os.path.exists(txt_file):
                # 读取文本文件内容
                with open(txt_file, "r") as f:
                    segments = f.readlines()

                # 输出 .lrc 文件路径
                output_file = os.path.join(output_directory, os.path.splitext(file)[0] + ".lrc")

                # 生成 .lrc 文件
                transcribe_audio_to_lrc(audio_file, segments, output_file)
            else:
                print(f"未找到对应的文本文件：{txt_file}")


if __name__ == "__main__":
    # 指定音频文件所在目录
    audio_directory = "../../temp/2:2nd合并后完整的mp3(2生成)/"
    # 指定文本文件所在目录
    text_directory = "../../temp/2nd合并后生成:初始文本[执行3rd]/"
    # 指定输出 .lrc 文件所在目录
    output_directory = "../../temp/3rd:1生成:字幕文件(自动)/"

    # 创建输出目录（如果不存在）
    os.makedirs(output_directory, exist_ok=True)

    # 批量处理生成 .lrc 文件
    batch_process_lrc(audio_directory, text_directory, output_directory)