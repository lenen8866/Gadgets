import configparser
import hashlib
import os
from time import sleep
from tkinter import Tk
from tkinter import filedialog
import requests

appId = None
accessToken = None
inputPath = None
outputPath = None
lang = None
voiceType = None

task_list = []

voiceTypeNameMap = {
    '1': '灿灿 2.0',
    '2': '炀炀',
    '3': '擎苍 2.0',
    '4': '通用女声 2.0',
    '5': '灿灿',
    '6': '超自然音色-梓梓2.0',
    '7': '超自然音色-梓梓',
    '8': '超自然音色-燃燃2.0',
    '9': '超自然音色-燃燃',
    '10': '通用女声',
    '11': '通用男声',
    '12': '擎苍',
    '13': '阳光青年',
    '14': '反卷青年',
    '15': '通用赘婿',
    '16': '古风少御',
    '17': '霸气青叔',
    '18': '质朴青年',
    '19': '温柔淑女',
    '20': '开朗青年',
    '21': '甜宠少御',
    '22': '儒雅青年',
    '23': '甜美小源',
    '24': '亲切女声',
    '25': '知性女声',
    '26': '诚诚',
    '27': '童童',
    '28': '亲切男声',
    '29': '译制片男声',
    '30': '懒小羊',
    '31': '清新文艺女声',
    '32': '鸡汤女声',
    '33': '智慧老者',
    '34': '慈爱姥姥',
    '35': '说唱小哥',
    '36': '活力解说男',
    '37': '影视解说小帅',
    '38': '解说小帅-多情感',
    '39': '影视解说小美',
    '40': '纨绔青年',
    '41': '直播一姐',
    '42': '反卷青年',
    '43': '沉稳解说男',
    '44': '潇洒青年',
    '45': '阳光男声',
    '46': '活泼女声',
    '47': '小萝莉',
    '48': '奶气萌娃',
    '49': '动漫海绵',
    '50': '动漫海星',
    '51': '动漫小新',
    '52': '天才童声',
    '53': '促销男声',
    '54': '促销女声',
    '55': '磁性男声',
    '56': '新闻女声',
    '57': '新闻男声',
    '58': '知性姐姐-双语',
    '59': '温柔小哥',
}

voiceTypeValueMap = {
    '1': 'BV700_V2_streaming',
    '2': 'BV705_streaming',
    '3': 'BV701_V2_streaming',
    '4': 'BV001_V2_streaming',
    '5': 'BV700_streaming',
    '6': 'BV406_V2_streaming',
    '7': 'BV406_streaming',
    '8': 'BV407_V2_streaming',
    '9': 'BV407_streaming',
    '10': 'BV001_streaming',
    '11': 'BV002_streaming',
    '12': 'BV701_streaming',
    '13': 'BV123_streaming',
    '14': 'BV120_streaming',
    '15': 'BV119_streaming',
    '16': 'BV115_streaming',
    '17': 'BV107_streaming',
    '18': 'BV100_streaming',
    '19': 'BV104_streaming',
    '20': 'BV004_streaming',
    '21': 'BV113_streaming',
    '22': 'BV102_streaming',
    '23': 'BV405_streaming',
    '24': 'BV007_streaming',
    '25': 'BV009_streaming',
    '26': 'BV419_streaming',
    '27': 'BV415_streaming',
    '28': 'BV008_streaming',
    '29': 'BV408_streaming',
    '30': 'BV426_streaming',
    '31': 'BV428_streaming',
    '32': 'BV403_streaming',
    '33': 'BV158_streaming',
    '34': 'BV157_streaming',
    '35': 'BR001_streaming',
    '36': 'BV410_streaming',
    '37': 'BV411_streaming',
    '38': 'BV437_streaming',
    '39': 'BV412_streaming',
    '40': 'BV159_streaming',
    '41': 'BV418_streaming',
    '42': 'BV120_streaming',
    '43': 'BV142_streaming',
    '44': 'BV143_streaming',
    '45': 'BV056_streaming',
    '46': 'BV005_streaming',
    '47': 'BV064_streaming',
    '48': 'BV051_streaming',
    '49': 'BV063_streaming',
    '50': 'BV417_streaming',
    '51': 'BV050_streaming',
    '52': 'BV061_streaming',
    '53': 'BV401_streaming',
    '54': 'BV402_streaming',
    '55': 'BV006_streaming',
    '56': 'BV011_streaming',
    '57': 'BV012_streaming',
    '58': 'BV034_streaming',
    '59': 'BV033_streaming',
}


def get_or_default(config, section, key, default=None):
    try:
        return config.get(section, key)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default


def init_config():
    # 创建一个配置解析器对象
    config = configparser.ConfigParser()
    section = 'DEFAULT'
    # 读取同文件夹下的配置文件
    try:
        # 尝试读取配置文件
        config.read('config.ini')
        global appId, accessToken, lang, voiceType, inputPath, outputPath
        appId = config.get(section, "app_id")
        accessToken = config.get(section, "access_token")
        lang = get_or_default(config, section, "lang", "cn")
        voiceType = get_or_default(config, section, "voice_type")
        inputPath = get_or_default(config, section, "input_path")
        outputPath = get_or_default(config, section, "output_path")
        if inputPath is not None and os.path.exists(inputPath) is False:
            inputPath = None
        if outputPath is not None and os.path.exists(outputPath) is False:
            outputPath = None
        # if voiceType not in voiceTypeValueMap.values():
        #     voiceType = None
        if lang not in ["cn", "en"]:
            lang = None
    except FileNotFoundError:
        print("配置文件未找到")
        input("执行完成，任意键退出")
        exit(1)
    except configparser.ParsingError:
        print("配置文件解析错误")
        input("执行完成，任意键退出")
        exit(1)
    except configparser.NoOptionError:
        print(f"配置项不存在")
        input("执行完成，任意键退出")
        exit(1)
    except Exception as e:
        print(f"发生了一个未知异常：{e}")
        input("执行完成，任意键退出")
        exit(1)


def string_hash(s):
    sha256 = hashlib.sha256()
    sha256.update(s.encode('utf-8'))
    return sha256.hexdigest().upper()


def get_voice_type():
    print("请选择发音人")
    for k in voiceTypeNameMap.keys():
        print(f"[{k}]{voiceTypeNameMap[k]}")
    choice = input("请输入发音人序号：")
    if choice not in voiceTypeValueMap.keys():
        print("输出无效")
        return get_voice_type()
    print(f"您选择的发音人为：{voiceTypeNameMap[choice]}")
    return voiceTypeValueMap[choice]


def get_lang():
    print("请选择语言")
    print("[1]CN")
    print("[2]EN")
    choice = input("请输入语言序号：")
    if choice not in ["1", "2"]:
        return get_lang()
    lang_map = {
        "1": "cn",
        "2": "en"
    }
    print(f"您选择的语言为：{lang_map[choice]}")
    return lang_map[choice]


def create_async_task(content, voice_type):
    url = "https://openspeech.bytedance.com/api/v1/tts_async/submit"

    hash_value = string_hash(content)

    payload = {
        "appid": appId,
        "reqid": hash_value,
        "text": content,
        "format": "mp3",
        "voice_type": voice_type,
        "language": lang
    }
    headers = {
        'Resource-Id': "volc.tts_async.default",
        'Authorization': f"Bearer; {accessToken}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    result = response.json()
    if "code" in result.keys():
        if result['code'] != 0 and result['code'] != 40004:
            print(f"调用API失败:{result['message']}")
            input("执行完成，任意键退出")
            exit(1)
    return hash_value


def query_task(task_id, file_path):
    url = "https://openspeech.bytedance.com/api/v1/tts_async/query"

    querystring = {"appid": appId, "task_id": task_id}

    payload = ""
    headers = {
        "Resource-Id": "volc.tts_async.default",
        "Authorization": f"Bearer; {accessToken}"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    result = response.json()
    global task_list
    if "code" in result.keys():
        print(f"任务未完成:{result['message']}")
        task_list.append({"task_id": task_id, "file_path": file_path})
    else:
        if "audio_url" in result.keys():
            download_file(result['audio_url'], file_path)
        else:
            print("任务未完成")
            task_list.append({"task_id": task_id, "file_path": file_path})


def download_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)


def get_input_folder():
    # 选择输入文件夹
    input_folder = filedialog.askdirectory(title="选择输入文件夹（不支持子文件夹）")
    if not input_folder:
        print("未选择输入文件夹，程序退出。")
        input("执行完成，任意键退出")
        exit(0)
    return input_folder


def get_output_folder():
    # 选择输入文件夹
    output_folder = filedialog.askdirectory(title="选择输出文件夹")
    if not output_folder:
        print("未选择输出文件夹，程序退出。")
        input("执行完成，任意键退出")
        exit(0)
    return output_folder


def process_txt_file(input_file, output_file, flag=False):
    # 打开文件
    with open(input_file, 'r', encoding='utf-8') as file:
        # 读取文件内容
        content = file.read()
        print("文本长度：" + str(len(content)))
        if flag:
            if len(content) > 1024:
                task_id = create_async_task(content, voiceType)
                sleep(0.1)
                global task_list
                task_list.append({"task_id": task_id, "file_path": output_file})
            else:
                process_file(content, output_file)


def process_file(content, out_file_path):
    url = "https://openspeech.bytedance.com/api/v1/tts"

    payload = {
        "app": {
            "appid": appId,
            "token": accessToken,
            "cluster": "volcano_tts"
        },
        "user": {"uid": "uid"},
        "audio": {
            "voice_type": voiceType,
            "encoding": "mp3",
            "compression_rate": 1,
            "rate": 24000,
            "speed_ratio": 1,
            "volume_ratio": 1,
            "pitch_ratio": 1,
            "language": lang
        },
        "request": {
            "reqid": string_hash(content),
            "text": content,
            "text_type": "ssml" if content.startswith("<speak>") else "plain",
            "operation": "query",
            "silence_duration": "125",
            "with_frontend": "1",
            "frontend_type": "unitTson",
            "pure_english_opt": "1"
        }
    }
    headers = {
        "Resource-Id": "volc.tts_async.default",
        "Authorization": f"Bearer; {accessToken}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    result = response.json()
    if result['code'] == 3000:
        import base64

        # 对base64字符串进行解码
        decoded_bytes = base64.b64decode(result['data'])

        # 将解码后的字符串写入文件
        with open(out_file_path, "wb") as file:
            file.write(decoded_bytes)

    else:
        print(f"请求异常{result['message']}")
        input("执行完成，任意键退出")
        exit(1)


def deal_async_task():
    global task_list
    while len(task_list) > 0:
        v = task_list.pop()
        query_task(v['task_id'], v['file_path'])
        sleep(0.5)


def main():
    init_config()
    # 创建Tkinter窗口但不显示
    root = Tk()
    root.withdraw()

    # 输入文件夹
    if inputPath is not None:
        input_folder = inputPath
    else:
        input_folder = get_input_folder()
        print("输入文件夹：" + input_folder)
    if outputPath is not None:
        output_folder = outputPath
    else:
        # 输出文件夹
        output_folder = get_input_folder()
        print("输出文件夹" + output_folder)
    global voiceType, lang
    if voiceType is None:
        voiceType = get_voice_type()

    if lang is None:
        lang = get_lang()

    print("开始处理")

    # 遍历输入文件夹中的txt文件
    for file in os.listdir(input_folder):
        if file.endswith(".txt"):
            print("发现文本文件：" + file)
            input_file = os.path.join(input_folder, file)
            output_file = os.path.join(output_folder, file[:-3] + "mp3")
            process_txt_file(input_file, output_file)
    choice = input("是否执行?(Y/N)")
    if choice != "Y":
        exit(0)
    for file in os.listdir(input_folder):
        if file.endswith(".txt"):
            input_file = os.path.join(input_folder, file)
            output_file = os.path.join(output_folder, file[:-3] + "mp3")
            process_txt_file(input_file, output_file, True)
    deal_async_task()


if __name__ == "__main__":
    main()
    input("执行完成，任意键退出")
