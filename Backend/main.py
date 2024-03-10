import os
import sys
import glob
import uuid
import webvtt
import requests

from moviepy.editor import AudioFileClip, ImageClip, TextClip, CompositeVideoClip, CompositeAudioClip, concatenate_videoclips
from datetime import datetime
from gpt import *

# 設定 subject 主題
subject = "sd記憶卡的發明"

# 語音模型 女 zh-TW-HsiaoChenNeural 女 zh-TW-HsiaoYuNeural 男 zh-TW-YunJheNeural
voice = "zh-TW-HsiaoChenNeural"

# 設定字體
FONT = "../fonts/PingFang.ttc"

# 背景音樂
SONG = "../Songs/Cliffsides.mp3"

# 指定要清除的檔案模式
file_pattern_temp = "../temp/*"

# 找到所有匹配的檔案
temp_files = glob.glob(file_pattern_temp)

# 刪除所有找到的檔案
for temp_file in temp_files:
    if os.path.isfile(temp_file):
        os.remove(temp_file)

# 指定要清除的檔案模式
file_pattern_output = "../output*"

# 找到所有匹配的檔案
output_files = glob.glob(file_pattern_output)

# 刪除所有找到的檔案
for output_file in output_files:
    if os.path.isfile(output_file):
        os.remove(output_file)

# 用 openai 模型生成回應
response_script = generate_response(subject)
print(response_script)

# 用 openai 模型生成生成圖片的句子
search_terms = generate_search_terms(response_script, subject)
print(search_terms)

def generate_image(prompt):
    images = []
    ROOT_DIR = os.path.dirname(sys.path[0])
    url = f"https://hercai.onrender.com/prodia/text2image?prompt={prompt}"
    r = requests.get(url)
    parsed = r.json()

    # 檢查 "url" 鍵是否存在於 parsed 字典中
    if "url" not in parsed:
        print(f"Error: The response does not contain a 'url' key. Response: {parsed}")
        return None

    image_url = parsed["url"]
    image_path = os.path.join(ROOT_DIR, "temp", str(uuid.uuid4()) + ".png")
    with open(image_path, "wb") as image_file:
        # 將位元組寫入文件
        image_r = requests.get(image_url)
        image_file.write(image_r.content)
        images.append(image_path)
    return image_path

for search_term in search_terms:
    generate_image(search_term)

# 要轉換的文字
text = response_script

# 輸出的語音檔案名稱
output_media = "../output.mp3"

# 輸出的字幕檔案名稱
output_subtitles = "../output.vtt"

# 執行 edge-tts 命令
os.system(f"edge-tts --text \"{text}\" --voice {voice} --rate=+10% --write-media {output_media} --write-subtitles {output_subtitles}")
                
# 讀取 VTT 檔案
with open("../output.vtt", "r") as file:
    lines = file.readlines()

# 將每一行的空格替換為無空格
new_lines = [line.replace(" ", "") for line in lines]

# 將新的字串寫回到檔案中
with open("../output1.vtt", "w") as file:
    file.writelines(new_lines)

# 指定要列出所有檔案的目錄
directory = "../temp"

# 使用 os.listdir 獲取目錄中的檔案名稱
imgs = os.listdir(directory)
img_files = [os.path.join(directory, img) for img in imgs if img.endswith(".png")]

# 讀取所有圖片檔案並調整大小
for img_file in img_files:
    img = ImageClip(img_file)
    img.fps = 24  # 指定每秒幀數為 24
    resized_img = img.resize((1080, 1920))  # 調整為 1080x1920

    # 寫出新的圖片檔案
    output_file = os.path.join(directory, f"resized_{os.path.basename(img_file)}")
    resized_img.save_frame(output_file)

# 重新獲取所有開頭為 resized 的照片檔案
imgs = os.listdir(directory)
img_files = [os.path.join(directory, img) for img in imgs if img.startswith("resized_")]

# 讀取音訊檔案
audio = AudioFileClip("../output.mp3")
background_music = AudioFileClip(SONG)

# 調整 background_music 音訊的長度
background_music = background_music.subclip(0, audio.duration)  # 將音訊的長度調整為與影片相同

# 調整 background_music 的音量
background_music = background_music.volumex(0.1)  # 將音訊的音量調整為原來的 10%

# 將音訊檔案合併成一個
combined_audio = CompositeAudioClip([audio, background_music])

# 獲取音訊的長度
audio_duration = audio.duration

# 讀取所有照片檔案
resize_imgs = [ImageClip(img).set_duration(audio_duration/5) for img in img_files]

# 將所有照片檔案組合成一個影片
combined_video = concatenate_videoclips(resize_imgs, method="compose")
combined_video.fps = 24  # 指定每秒幀數為 24

# 將音訊添加到合併後的影片中
final_video = combined_video.set_audio(combined_audio)

# 讀取 VTT 檔案
subs = webvtt.read('../output1.vtt')

# 為每一個字幕創建一個 TextClip
clips = []
for sub in subs:
    # 將時間轉換為秒數
    start = datetime.strptime(sub.start, '%H:%M:%S.%f') - datetime(1900, 1, 1)
    end = datetime.strptime(sub.end, '%H:%M:%S.%f') - datetime(1900, 1, 1)
    start_seconds = start.total_seconds()
    end_seconds = end.total_seconds()

    # 創建 TextClip
    clip = TextClip(sub.text, font=FONT, fontsize=40, color='black', bg_color='white', stroke_color='yellow', stroke_width=1).set_start(start_seconds).set_duration(end_seconds - start_seconds).set_position(('center', 'center'))
    clips.append(clip)


# 將字幕添加到影片中
final_video_with_subs = CompositeVideoClip([final_video] + clips)

# 寫出新的影片檔案
final_video_with_subs.write_videofile("../output_with_subs.mp4")