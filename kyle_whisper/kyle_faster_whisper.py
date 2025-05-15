
##############################
''''

Faster Whisper：同样不完全支持实时流式输入，但它的加速性能使得在分批处理时能够显著减少延迟。如果你把音频分成小段并逐步处理，Faster Whisper 会比原版 Whisper 更适合低延迟任务。

Faster Whisper 都能够识别包括但不限于 英语、法语、西班牙语、德语、中文、日语、俄语等多种语言，且能应对 各种口音和方言。
英语口音：无论是英式英语、美国英语，还是印度口音等，Whisper 和 Faster Whisper 都有很强的适应能力。
非英语口音：Whisper 和 Faster Whisper 对其他语言（如法语、德语等）也有较好的识别能力，能够处理一定程度的地方方言。

Whisper速度
模型	速度体验	推荐场景
tiny / base	几乎实时或接近实时	小程序、实时字幕
small	稍微慢一点，但还能接受	正常应用
medium / large	很慢，不适合实时	离线转录、大型数据处理
'''

# https://github.com/SYSTRAN/faster-whisper

import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from faster_whisper import  WhisperModel
import time
import torch

# print(torch.cuda.is_available())  # True 代表 CUDA 可用
# print(torch.cuda.device_count())  # 你的 GPU 数量
# print(torch.cuda.get_device_name(0))  # 你的 GPU 名称
#
#
# exit()

def kyle_faster_whisper_1(model_type: str= "tiny",
                          abs_path:str="",
                          beam_size: int=5,
                          # language: str=None,
                          task: str="transcribe",
                          compute_type: str="float16",
                          device: str="cuda" if torch.cuda.is_available() else "cpu"
                          ) -> tuple[list[str], list[str]]:
    
    # model_type: ["tiny", "base", "small", "medium", "large-v2", "large-v3"]

    if not abs_path:
        raise ValueError("abs_path is required!")
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"The file at {abs_path} was not found!")

    # Validating model_type
    # valid_model_types = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]
    # if model_type not in valid_model_types:
    #     raise ValueError(f"Invalid model_type: {model_type}. \nValid options are: {valid_model_types}")

    # validating dev
    if (torch.cuda.is_available()) and (device == "cuda") and (compute_type in ["int8_float16","float16","float32","int8"]):
        model = WhisperModel(model_type, device="cuda", compute_type=compute_type) # cude support: int8 \ float16 \ float32 \ int8_float16

    elif (device == "cpu") and (compute_type in ["float32","int8"]):
        model = WhisperModel(model_type, device="cpu", compute_type=compute_type)   # cpu support:  int8  \ float32 \

    elif (device == "cpu") and (compute_type in ["float16","int8_float16"]):
        print(r"cpu:  int8_float16 and float16 not support, int8 will be used")
        model = WhisperModel(model_type, device="cpu", compute_type="int8")


    segments, _ = model.transcribe(audio=abs_path,
                                   beam_size=beam_size,
                                   task=task, # transcribe OR translate
                                   # vad_filter=True,
                                   )
    # task: 默认是transcribe，即输出同语言转写，，，，可设置translate，从xxxx 翻译为 英文
    # task: Task to execute (transcribe or translate).
    # vad_filter：启用语音活动检测（VAD），以过滤无语音部分。该步骤使用 Silero VAD 模型（GitHub）。
    # log_progress: whether to show progress bar or not.
    #
#
# '''
# 参数翻译：
#
#     audio：输入文件路径（或类似文件对象），或者音频波形。
#
#     language：音频中的语言，使用语言代码（如 "en" 或 "fr"）。如果未设置，将在音频的前 30 秒内进行检测。
#
#     task：执行的任务（转录或翻译）。
#
#     log_progress：是否显示进度条。
#
#     beam_size：用于解码的 beam size（束搜索大小）。
#
#     best_of：在非零温度采样时使用的候选数量。
#
#     patience：束搜索的耐心因子。
#
#     length_penalty：指数长度惩罚常数。
#
#     repetition_penalty：对之前生成的 token 分数施加惩罚（设定 > 1 以惩罚）。
#
#     no_repeat_ngram_size：防止 n-gram 重复，设定为 0 时禁用。
#
#     temperature：用于采样的温度，可为一个温度元组，若失败，则依照 compression_ratio_threshold 或 log_prob_threshold 依次使用。
#
#     compression_ratio_threshold：如果 gzip 压缩比超过该值，则视为失败。
#
#     log_prob_threshold：如果采样 token 的平均对数概率低于该值，则视为失败。
#
#     no_speech_threshold：如果无语音概率高于该值且平均对数概率低于 log_prob_threshold，则认为该片段是静音。
#
#     condition_on_previous_text：如果为 True，则模型的前一次输出将作为下一个窗口的提示；禁用此选项可能会导致文本在不同窗口之间不一致，但可能减少模型陷入失败循环（如重复循环或时间戳不同步）。
#
#     prompt_reset_on_temperature：如果温度高于该值，则重置提示，仅在 condition_on_previous_text 为 True 时生效。
#
#     initial_prompt：可选的文本字符串或 token ID 迭代器，用作第一个窗口的提示。
#
#     prefix：可选的文本前缀，作为第一个窗口的起始文本。
#
#     suppress_blank：在采样开始时抑制空白输出。
#
#     suppress_tokens：要抑制的 token ID 列表，-1 将抑制 tokenizer.non_speech_tokens() 定义的默认符号。
#
#     without_timestamps：仅采样文本 token。
#
#     max_initial_timestamp：初始时间戳不能晚于此值。
#
#     word_timestamps：使用交叉注意力模式和动态时间规整（DTW）提取单词级时间戳，并在每个片段中包含各个单词的时间戳。
#
#     prepend_punctuations：如果 word_timestamps 为 True，则将这些标点符号与下一个单词合并。
#
#     append_punctuations：如果 word_timestamps 为 True，则将这些标点符号与前一个单词合并。
#
#     multilingual：对每个片段进行语言检测。
#
#     vad_filter：启用语音活动检测（VAD），以过滤无语音部分。该步骤使用 Silero VAD 模型（GitHub）。
#
#     vad_parameters：Silero VAD 参数字典或 VadOptions 类（可查看 VadOptions 类中的可用参数和默认值）。
#
#     max_new_tokens：每个片段生成的新 token 最大数量，若未设置，则使用默认 max_length。
#
#     chunk_length：音频片段的长度。若设置，会覆盖 FeatureExtractor 的默认 chunk_length。
#
#     clip_timestamps：以逗号分隔的时间戳 start,end,start,end,...（秒），指定需要处理的音频片段。最后一个结束时间戳默认设置为文件结尾。使用 clip_timestamps 时会忽略 vad_filter。
#
#     hallucination_silence_threshold：当 word_timestamps 为 True 时，如果检测到可能的幻觉并且静音时间超过该阈值（秒），则跳过该静音段。
#
#     hotwords：提供给模型的热词或提示短语。若 prefix 不为 None，此参数无效。
#
#     language_detection_threshold：如果语言 token 最大概率高于该值，则判定语言检测成功。
#
#     language_detection_segments：用于语言检测的片段数量。
#
# '''


    ############### info is class ##############
    # language + language_probability	自动语言识别结果
    # duration + duration_after_vad	音频总时长 & 有效语音时长
    # all_language_probs	多语言识别概率分布
    # transcription_options	控制转写的参数（模型、翻译等）
    # vad_options	控制语音活动检测的行为

    context1 = []
    context2 = []

    for segment in segments:
        # print(f"\n\n[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        context1.append(segment.text)
        context2.append(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
    return context1, context2







def kyle_faster_whisper_0(model_type="tiny", abs_path=""):
    # Check if the file path exists
    if not abs_path:
        raise ValueError("abs_path is required!")
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"The file at {abs_path} was not found!")

    # Validating model_type
    valid_model_types = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]
    if model_type not in valid_model_types:
        raise ValueError(f"Invalid model_type. Valid options are: {', '.join(valid_model_types)}")

    # Measure model loading time
    t1 = time.time()
    if torch.cuda.is_available() :
        print("torch.cuda.is_available(): ",torch.cuda.is_available())  # True means CUDA is available
        # print("torch.cuda.device_count(): ", torch.cuda.device_count())  # Number of GPUs
        # print("torch.cuda.get_device_name(0): ", torch.cuda.get_device_name(0))  # GPU Name
        model = WhisperModel(model_type, device="cuda", compute_type="float32")
        model = WhisperModel(model_type, device="cuda", compute_type="float16")
        model = WhisperModel(model_type, device="cuda", compute_type="int8_float16")
        model = WhisperModel(model_type, device="cuda", compute_type="int8")


    elif not torch.cuda.is_available() :
        model = WhisperModel(model_type, device="cpu", compute_type="float32")
        # model = WhisperModel(model_type, device="cpu", compute_type="float16")  # not support
        # modelc816 = WhisperModel(model_type, device="cpu", compute_type="int8_float16") # not support
        # model = WhisperModel(model_type, device="cpu", compute_type="int8")

    t2 = time.time()
    print(f"\nModel loading time: {t2 - t1:.6f} seconds")

    # Measure transcription time
    t3 = time.time()
    segments, info = model.transcribe(audio=abs_path,
                                      beam_size=5,
                                     # language="None",
                                      task="translate",  # translate   transcribe
                                      vad_filter=True,
                                      # log_progress=True
                                      )
    # task: 默认是transcribe，即输出同语言转写，，，，可设置translate，从xxxx 翻译为 英文
    # task: Task to execute (transcribe or translate).
    # vad_filter：启用语音活动检测（VAD），以过滤无语音部分。该步骤使用 Silero VAD 模型（GitHub）。
    # log_progress: whether to show progress bar or not.
    #
#
# '''
# 参数翻译：
#
#     audio：输入文件路径（或类似文件对象），或者音频波形。
#
#     language：音频中的语言，使用语言代码（如 "en" 或 "fr"）。如果未设置，将在音频的前 30 秒内进行检测。
#
#     task：执行的任务（转录或翻译）。
#
#     log_progress：是否显示进度条。
#
#     beam_size：用于解码的 beam size（束搜索大小）。
#
#     best_of：在非零温度采样时使用的候选数量。
#
#     patience：束搜索的耐心因子。
#
#     length_penalty：指数长度惩罚常数。
#
#     repetition_penalty：对之前生成的 token 分数施加惩罚（设定 > 1 以惩罚）。
#
#     no_repeat_ngram_size：防止 n-gram 重复，设定为 0 时禁用。
#
#     temperature：用于采样的温度，可为一个温度元组，若失败，则依照 compression_ratio_threshold 或 log_prob_threshold 依次使用。
#
#     compression_ratio_threshold：如果 gzip 压缩比超过该值，则视为失败。
#
#     log_prob_threshold：如果采样 token 的平均对数概率低于该值，则视为失败。
#
#     no_speech_threshold：如果无语音概率高于该值且平均对数概率低于 log_prob_threshold，则认为该片段是静音。
#
#     condition_on_previous_text：如果为 True，则模型的前一次输出将作为下一个窗口的提示；禁用此选项可能会导致文本在不同窗口之间不一致，但可能减少模型陷入失败循环（如重复循环或时间戳不同步）。
#
#     prompt_reset_on_temperature：如果温度高于该值，则重置提示，仅在 condition_on_previous_text 为 True 时生效。
#
#     initial_prompt：可选的文本字符串或 token ID 迭代器，用作第一个窗口的提示。
#
#     prefix：可选的文本前缀，作为第一个窗口的起始文本。
#
#     suppress_blank：在采样开始时抑制空白输出。
#
#     suppress_tokens：要抑制的 token ID 列表，-1 将抑制 tokenizer.non_speech_tokens() 定义的默认符号。
#
#     without_timestamps：仅采样文本 token。
#
#     max_initial_timestamp：初始时间戳不能晚于此值。
#
#     word_timestamps：使用交叉注意力模式和动态时间规整（DTW）提取单词级时间戳，并在每个片段中包含各个单词的时间戳。
#
#     prepend_punctuations：如果 word_timestamps 为 True，则将这些标点符号与下一个单词合并。
#
#     append_punctuations：如果 word_timestamps 为 True，则将这些标点符号与前一个单词合并。
#
#     multilingual：对每个片段进行语言检测。
#
#     vad_filter：启用语音活动检测（VAD），以过滤无语音部分。该步骤使用 Silero VAD 模型（GitHub）。
#
#     vad_parameters：Silero VAD 参数字典或 VadOptions 类（可查看 VadOptions 类中的可用参数和默认值）。
#
#     max_new_tokens：每个片段生成的新 token 最大数量，若未设置，则使用默认 max_length。
#
#     chunk_length：音频片段的长度。若设置，会覆盖 FeatureExtractor 的默认 chunk_length。
#
#     clip_timestamps：以逗号分隔的时间戳 start,end,start,end,...（秒），指定需要处理的音频片段。最后一个结束时间戳默认设置为文件结尾。使用 clip_timestamps 时会忽略 vad_filter。
#
#     hallucination_silence_threshold：当 word_timestamps 为 True 时，如果检测到可能的幻觉并且静音时间超过该阈值（秒），则跳过该静音段。
#
#     hotwords：提供给模型的热词或提示短语。若 prefix 不为 None，此参数无效。
#
#     language_detection_threshold：如果语言 token 最大概率高于该值，则判定语言检测成功。
#
#     language_detection_segments：用于语言检测的片段数量。
#
# '''


    ############### info is class ##############
    # language + language_probability	自动语言识别结果
    # duration + duration_after_vad	音频总时长 & 有效语音时长
    # all_language_probs	多语言识别概率分布
    # transcription_options	控制转写的参数（模型、翻译等）
    # vad_options	控制语音活动检测的行为

    t4 = time.time()
    # print(f"\n{segments}")
    # print(f"\n{info.all_language_probs}")
    # print(f"\n{info.transcription_options}")
    # print(f"\n{info.vad_options}")
    #
    #
    print(f"\n\nModel transcribe time: {t4 - t3:.6f} seconds")
    # print(f"\n\nDetected language '{info.language}' with probability {info.language_probability:.2f}")

    # Collect transcribed text and print segments
    context = []
    for segment in segments:
        print(f"\n\n[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        context.append(segment.text)
    print("\n\nContext:", context)
    return context





if __name__ == "__main__":

    try:
        a1,a2 = kyle_faster_whisper_1(model_type="large",
                                  abs_path="./video/2.mp3",
                                  task="transcribe",
                                  compute_type="int8",
                                  device="cuda",)
        print(a1)
        print(a2)

    except Exception as e:
        print(f"Error: {e}")




    # Example usage
    # try:
    #     result = kyle_faster_whisper_0(model_type="tiny", abs_path="./audio_recording/61-70970-0000.flac")
    # except Exception as e:
    #     print(f"Error: {e}")