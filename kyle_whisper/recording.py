# import tkinter as tk
# import time
# import os
#
# def reset_buttons():
#     b_start.config(state=tk.NORMAL)
#     b_pause.config(state=tk.DISABLED)
#     b_resume.config(state=tk.DISABLED)
#     b_end.config(state=tk.DISABLED)
#
# def reset_timer():
#     global timer_running, start_time, paused_time
#     timer_running = False
#     start_time = 0
#     paused_time = 0
#     label_time.config(text="00:00:00")
#
# def on_start():
#     global timer_running, start_time
#     start_time = time.time() - paused_time  # 计算从暂停时的起始时间
#     timer_running = True
#     update_timer()  # 启动计时器
#     b_start.config(state=tk.DISABLED)
#     b_pause.config(state=tk.NORMAL)
#     b_end.config(state=tk.NORMAL)
#
# def on_pause():
#     global timer_running, paused_time
#     timer_running = False
#     paused_time = time.time() - start_time  # 记录暂停时的时间
#     b_pause.config(state=tk.DISABLED)
#     b_resume.config(state=tk.NORMAL)
#
# def on_resume():
#     global timer_running, start_time
#     start_time = time.time() - paused_time  # 恢复计时
#     timer_running = True
#     update_timer()  # 启动计时器
#     b_resume.config(state=tk.DISABLED)
#     b_pause.config(state=tk.NORMAL)
#
# def on_end():
#     reset_timer()  # 重置计时器
#     reset_buttons()  # 重置按钮状态
#
# def update_timer():
#     if timer_running:
#         elapsed_time = time.time() - start_time
#         minutes, seconds = divmod(elapsed_time, 60)
#         hours, minutes = divmod(minutes, 60)
#         time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
#         label_time.config(text=time_str)
#         root.after(1000, update_timer)  # 每秒钟更新一次计时器


import tkinter as tk
import time
import os
from os.path import exists

import pyaudio
import wave
import threading
from datetime import datetime

# 设置录音参数
FORMAT = pyaudio.paInt16  # 16位深度
# FORMAT = pyaudio.paInt16  # 16位深度,,使用 8 位（paInt8），音频质量较差，但文件会更小,,使用 32 位（paInt32），音频质量更好，但文件会更大
#
CHANNELS = 1  # 单声道
# CHANNELS = 1  # 单声道,,
# CHANNELS = 2 表示立体声（Stereo）,文件较大，但提供更好的音频体验。如果录制的内容需要保留空间中的多个声道（例如音乐或环境声音），可以选择立体声。

RATE = 44100  # 采样率
# RATE = 44100  # 采样率 如果采样率过低（例如 22050 Hz 或更低），音频会失真，尤其是高频部分。
# # 如果采样率过高（例如 96000 Hz 或更高），虽然音质会更好，但文件大小也会大幅增加，而且对人耳的区别可能并不明显，尤其在录制普通语音时。
CHUNK = 1024  # 每次读取的音频块大小
'''
这是每次读取的音频块大小，也就是每次从音频流中读取的样本数量。
选择合适的 CHUNK 大小非常重要：
较小的 CHUNK（例如 512 或 256）可以降低延迟，但会增加处理频率，对性能要求较高。
较大的 CHUNK（例如 2048 或 4096）会减少处理的频率，减少CPU负担，但可能会增加延迟。
1024 是一个比较常用的值，平衡了延迟和性能。
'''

OUTPUT_FILENAME = f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.wav"  # 输出的文件名

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 全局变量
recording = False
paused = False
frames = []
start_time = 0
paused_time = 0
timer_running = False

# 创建主窗口
root = tk.Tk()
root.title("DUAN_recording")

# 检查并设置窗口图标
icon_path = "../img/plane.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# 设置窗口属性
root.attributes('-alpha', 0.95)  # 设置透明度
root.attributes('-topmost', 1)  # 置顶窗口

# 获取屏幕尺寸
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

# 计算窗口大小和位置
window_width = min(300, screen_width * 4 // 5)  # 4/5
window_height = min(140, screen_height // 6)
x_position = (screen_width - window_width) // 2
y_position = min((screen_height - window_height) * 3 // 6, screen_height - window_height - 50)

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
print(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.config(bg='black')
root.resizable(False, False)
root.minsize(window_width, window_height)

# 计时器更新函数
def update_timer():
    global timer_running, start_time,paused
    if timer_running and not paused:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        label_time.config(text=time_str)
    if timer_running:  # 不管暂停与否都继续回调（等待下次恢复）
        root.after(1000, update_timer)  # 每秒钟更新一次计时器

# 重置按钮
def reset_buttons():
    b_start.config(state=tk.NORMAL)
    b_pause.config(state=tk.DISABLED)
    b_resume.config(state=tk.DISABLED)
    b_end.config(state=tk.DISABLED)

# 重置计时器
def reset_timer():
    global timer_running, start_time, paused_time
    timer_running = False
    start_time = 0
    paused_time = 0
    label_time.config(text="00:00:00")

# 开始录音
def on_start():
    global recording, paused, frames, start_time, timer_running
    frames = []  # 清空录音缓存
    recording = True
    paused = False
    start_time = time.time() - paused_time
    timer_running = True
    update_timer()

    # 开启录音流
    def record():
        global paused
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        while recording:
            if not paused:
                data = stream.read(CHUNK)
                frames.append(data)
            time.sleep(0.01)  # 稍微等待，避免占用过多CPU

        stream.stop_stream()
        stream.close()

    threading.Thread(target=record, daemon=True).start()

    b_start.config(state=tk.DISABLED)
    b_pause.config(state=tk.NORMAL)
    b_end.config(state=tk.NORMAL)

# 暂停录音
def on_pause():
    global paused, paused_time
    paused = True
    paused_time = time.time() - start_time  # ✅ 记录暂停前已运行时间
    print("录音暂停...")
    b_pause.config(state=tk.DISABLED)
    b_resume.config(state=tk.NORMAL)

# 恢复录音
def on_resume():
    global paused, start_time
    paused = False
    start_time = time.time() - paused_time  # ✅ 恢复起点重新设定
    print("录音恢复...")
    b_resume.config(state=tk.DISABLED)
    b_pause.config(state=tk.NORMAL)


# 结束录音
def on_end():
    global recording
    recording = False
    save_recording()
    reset_timer()  # 重置计时器
    reset_buttons()  # 重置按钮状态

# 保存录音
def save_recording():
    os.makedirs(name="./video", exist_ok=True)
    filename = f"./video/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print(f"录音已保存为 {filename}")

# UI组件
fun_frame = tk.Frame(root, bg='#7FFFAA')
fun_frame.place(x=5, y=5, width=135, height=120)

label_time = tk.Label(fun_frame, bg='white', fg='black', text="00:00:00", font=("Times New Roman", 20))
label_time.place(x=5, y=25, width=125, height=60)

frame_setting = tk.Frame(root, bg='#7FFFAA')
frame_setting.place(x=145, y=5, width=150, height=120)

b_start = tk.Button(frame_setting, text='开始', command=on_start)
b_start.place(x=10, y=10, width=60, height=45)

b_pause = tk.Button(frame_setting, text='暂停', command=on_pause, state=tk.DISABLED)
b_pause.place(x=80, y=10, width=60, height=45)

b_resume = tk.Button(frame_setting, text='继续', command=on_resume, state=tk.DISABLED)
b_resume.place(x=10, y=65, width=60, height=50)

b_end = tk.Button(frame_setting, text='结束', command=on_end, state=tk.DISABLED)
b_end.place(x=80, y=65, width=60, height=50)

root.mainloop()

