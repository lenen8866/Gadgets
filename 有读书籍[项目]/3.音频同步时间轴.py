import speech_recognition as sr
from pydub import AudioSegment


def transcribe_audio_to_lrc(audio_file, segments):
    recognizer = sr.Recognizer()
    # 加载 mp3 文件
    audio = AudioSegment.from_mp3(audio_file)

    # 准备 lrc 输出格式的列表
    lrc_output = []

    # 用于跟踪时间轴的开始位置（毫秒）
    start_time_ms = 0

    # 获取音频的时长（毫秒）
    duration = len(audio)

    # 假设每个段落文本的时长是根据文本比例分配的
    total_text_length = sum(len(segment) for segment in segments)

    for segment in segments:
        # 根据文本长度的比例，计算每个文本片段的时长
        segment_duration = (len(segment) / total_text_length) * duration

        # 从音频中提取当前片段
        audio_chunk = audio[start_time_ms:int(start_time_ms + segment_duration)]

        # 暂存音频片段到临时文件
        temp_wav_file = "2nd_音频处理/火山语音合成/temp_segment.wav"
        audio_chunk.export(temp_wav_file, format="wav")

        # 识别当前音频片段中的文本
        with sr.AudioFile(temp_wav_file) as source:
            audio_data = recognizer.record(source)
            try:
                # 识别并生成时间戳
                minutes = start_time_ms // 60000
                seconds = (start_time_ms % 60000) / 1000

                # 格式化时间戳并与对应文本行关联
                lrc_line = f"[{int(minutes):02}:{seconds:05.2f}] {segment.strip()}"
                lrc_output.append(lrc_line)

                # 更新开始时间（毫秒）
                start_time_ms += segment_duration

            except sr.UnknownValueError:
                print("无法识别音频内容")
            except sr.RequestError as e:
                print(f"请求结果出错：{e}")

    # 将 lrc 格式的内容写入 .lrc 文件
    with open("output.lrc", "w") as f:
        for line in lrc_output:
            f.write(line + "\n")

    print("LRC 文件已生成：output.lrc")


# 要与音频同步的文本内容，逐行分割
segments = [
"""
Long,
long ago,
there were no boys or girls.
There were no mothers or fathers.
There was no earth with rivers and trees.
No one was there, but God.

God has always been.
God will always be.
There is God the Father.
There is God the Son.
We call Him Jesus.
And there is God the Holy Spirit.
There is one God but three persons.

God family is a little like our families.
A family is one family,
but there are different people in the family.
There is a father and a mother.
And there are children.

God made many angels to live with Him in heaven,
and to work with Him.
He made this world and put people in it.
God wanted angels and people to be His friends.
"""
]

# mp3 文件路径
audio_file = "/temp/mp3_text/Story_1:_From_the_Beginning.mp3"

# 调用函数生成 lrc 文件
transcribe_audio_to_lrc(audio_file, segments)