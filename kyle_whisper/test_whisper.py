
'''
Whisper 支持以下音频格式：
WAV、MP3、FLAC、M4A、OGG 等常见的音频格式。
支持不同的采样率，但通常推荐16kHz 或更高采样率以获得最佳效果。
对于 FLAC 格式，Whisper 也能高效处理，因为它是无损压缩格式，适合对音质要求较高的情况。

Whisper 本身的设计并不优化实时流式输入。换句话说，它并不完全支持实时语音识别（如边听边转录）。
在实际使用中，Whisper 处理的音频通常是批量加载后进行转录，这意味着它需要先将音频加载进内存，并在音频处理完后输出结果。
如果你希望实现类似实时转录的功能，可以尝试在音频流入时将音频切割成小段并分别进行转录。但这种做法可能会带来延迟，而且在实时性要求较高的场景下，Whisper 并不是最理想的选择。

Whisper 支持 多语言转录，包含：
英语、中文、法语、德语、日语、西班牙语、葡萄牙语、俄语等 几十种语言。
对于一些少数语言，Whisper 可能会显示较低的准确率，但它依然是一个非常强大的多语言语音识别系统。

5. 支持并行处理
Whisper 支持将不同的音频文件并行处理，特别是当你使用多线程或GPU时，可以显著提升处理效率。


口音表现：Whisper 对于英语的各种口音（如美国、英国、澳大利亚、印度英语等）有很好的适应性，能够处理各种方言和变种语言。

'''
# https://github.com/openai/whisper


import torch
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
import whisper
import time


t1 = time.perf_counter()
print(f"PyTorch版本: {torch.__version__}")

t2 = time.perf_counter()

print(f"CUDA可用: {torch.cuda.is_available()}")
t3 = time.perf_counter()

print(f"当前设备: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")
t4 = time.perf_counter()



t5= time.perf_counter()

model = whisper.load_model("tiny",device="cuda") # 加载模型
'''
# 加载不同的模型
https://github.com/openai/whisper
前面四个适用于英文
model_tiny = whisper.load_model("tiny")
model_base = whisper.load_model("base")
model_small = whisper.load_model("small")
model_medium = whisper.load_model("medium")

# 适合多语言
model_large = whisper.load_model("large")
model_large = whisper.load_model("turbo") # large-v3-turbo	large-v3  large-v2
'''
t6 = time.perf_counter()





# 转录 FLAC 文件
result = model.transcribe("./audio_recording/61-70970-0000.flac")
t7 = time.perf_counter()
# 打印转录结果
print(result["text"])


# 计算时间差，精确到微秒
# 输出精确到 6 位小数的时间（微秒级别）
print(f"Elapsed time: {t2-t1:.6f} seconds")
print(f"Elapsed time: {t3-t2:.6f} seconds")
print(f"Elapsed time: {t4-t3:.6f} seconds")
print(f"Elapsed time: {t5-t4:.6f} seconds")
print(f"load model time: {t6-t5:.6f} seconds")
print(f"translating time: {t7-t6:.6f} seconds")





