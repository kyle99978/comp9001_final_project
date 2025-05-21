import os
import time
import torch
from transformers import MarianMTModel, MarianTokenizer

# 禁用 HuggingFace 符号链接警告
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

# 语言对与模型的映射表
LANGUAGE_MODEL_MAPPING = {
    "中文 ➜ 英文": "Helsinki-NLP/opus-mt-zh-en",
    "英文 ➜ 中文": "Helsinki-NLP/opus-mt-en-zh",
    "日文 ➜ 英文": "Helsinki-NLP/opus-mt-ja-en",
    "英文 ➜ 日文": "Helsinki-NLP/opus-mt-en-ja",
    "韩文 ➜ 英文": "Helsinki-NLP/opus-mt-ko-en",
    "英文 ➜ 韩文": "Helsinki-NLP/opus-mt-en-ko",
    "法文 ➜ 英文": "Helsinki-NLP/opus-mt-fr-en",
    "英文 ➜ 法文": "Helsinki-NLP/opus-mt-en-fr",
}


def translate_text_with_time(
        task: str, text: str, device_setting: str = "auto", precision_setting: str = "fp32"
):
    """
    使用指定的翻译任务和输入文本进行翻译，并统计阶段时间。

    参数:
    ------
    task : str
        翻译任务的语言对（例如 "中文 ➜ 英文", "英文 ➜ 中文"）。
    text : str
        要翻译的输入文本。
    device_setting : str, optional
        设备类型，默认 "auto"（支持 "auto", "cpu", "cuda"）。
    precision_setting : str, optional
        精度选项，默认 "fp32"（支持 "fp32", "fp16", "int8"）。

    返回值:
    -------
    tuple : (str, list)
        - str: 翻译后的文本结果。
        - list: 包含各阶段时间的数组 [分词耗时, 翻译耗时, 解码耗时]。
    """
    '''
    Translates using the specified translation task and input text, and counts stage times.

    Parameters.
    ------
    task : str
        Language pair for the translation task (e.g. "Chinese ➜ English", "English ➜ Chinese").
    text : str
        Input text to be translated.
    device_setting : str, optional
        device_setting, default is "auto" (supports "auto", "cpu", "cuda").
    precision_setting : str, optional
        Precision options, default "fp32" (supports "fp32", "fp16", "int8").

    Return value.
    -------
    tuple : (str, list)
        - str: the result of the translated text.
        - list: an array containing the time of each stage [time spent on segmentation, time spent on translation, time spent on decoding].
    '''
    if task not in LANGUAGE_MODEL_MAPPING:
        raise ValueError(f"不支持的翻译任务: {task}")

    model_name = LANGUAGE_MODEL_MAPPING[task]

    # 开始模型加载时间
    model_load_start_time = time.time()

    # 确定设备
    if device_setting == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = device_setting
    print(f"正在使用设备: {device}")

    # 加载模型和设置精度
    if precision_setting == "fp16" and device == "cuda":
        model = MarianMTModel.from_pretrained(model_name, torch_dtype=torch.float16)
    elif precision_setting == "int8" and device == "cuda":
        from transformers import BitsAndBytesConfig
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        model = MarianMTModel.from_pretrained(model_name, quantization_config=quantization_config, device_map="auto")
    else:
        model = MarianMTModel.from_pretrained(model_name)  # 默认 fp32
    model = model.to(device)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    # 模型加载完成时间
    model_load_end_time = time.time()
    print(f"模型加载完成，耗时: {model_load_end_time - model_load_start_time:.4f} 秒")

    # 开始翻译的各阶段计时
    # 1. 分词和输入准备
    stage1_start_time = time.time()
    inputs = tokenizer([text], return_tensors="pt", padding=True).to(device)
    stage1_end_time = time.time()

    # 2. 翻译生成
    stage2_start_time = time.time()
    translated = model.generate(**inputs)
    stage2_end_time = time.time()

    # 3. 解码翻译结果
    stage3_start_time = time.time()
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    stage3_end_time = time.time()

    # 计算时间数组
    time_stats = [
        stage1_end_time - stage1_start_time,  # 分词和输入准备时间
        stage2_end_time - stage2_start_time,  # 翻译生成时间
        stage3_end_time - stage3_start_time,  # 解码翻译结果时间
    ]

    return translated_text, time_stats


def load_model(model_name,device_setting:str="auto",precision_setting:str="fp32"):

    # 开始模型加载时间
    model_load_start_time = time.time()

    # 确定设备
    if device_setting == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = device_setting
    print(f"正在使用设备: {device}")

    # 加载模型和设置精度
    if precision_setting == "fp16" and device == "cuda":
        model = MarianMTModel.from_pretrained(model_name, torch_dtype=torch.float16)
    elif precision_setting == "int8" and device == "cuda":
        from transformers import BitsAndBytesConfig
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        model = MarianMTModel.from_pretrained(model_name, quantization_config=quantization_config, device_map="auto")
    else:
        model = MarianMTModel.from_pretrained(model_name)  # 默认 fp32
    model = model.to(device)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    # 模型加载完成时间
    model_load_end_time = time.time()
    print(f"模型加载完成，耗时: {model_load_end_time - model_load_start_time:.4f} 秒")

    return  model, tokenizer, device

def translate_text(model, tokenizer, device, text):
    # max_length：限制生成的最长token数。    #
    # early_stopping = True： EOS，就立刻停止。
    # num_beams：使用  search，提高翻译质量。
    # no_repeat_ngram_size：禁止生成重复的n-gram。
    # repetition_penalty：对重复的词语加惩罚，降低它们的生成概率。

#     # 1. 分词并传入设备
#     inputs = tokenizer(
#         [text],
#         return_tensors="pt",
#         padding=True,
#         truncation=True,
#         max_length=128
#     ).to(device)
#
#     # 2. 带上生成控制参数
#     translated = model.generate(
#         **inputs,
#         max_length=50,             # 最多 50 个 token
#         early_stopping=True,       # 遇到 EOS 就停
#         num_beams=4,               # 4 路 beam search
#         no_repeat_ngram_size=2,    # 禁止 2-gram 重复
#         repetition_penalty=1.2,    # 重复惩罚
#     )
#
    inputs = tokenizer([text], return_tensors="pt", padding=True,truncation=True,max_length=128).to(device)
    # translated = model.generate(**inputs)
    translated = model.generate(
        **inputs,
        max_length=50,             # 最多 50 个 token
        early_stopping=True,       # 遇到 EOS 就停
        num_beams=4,               # 4 路 beam search
        no_repeat_ngram_size=2,    # 禁止 2-gram 重复
        repetition_penalty=1.2,    # 重复惩罚
    )

    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text


def start_trans_ZHtoEN(text: list[str]):
    model, tokenizer, device = load_model("Helsinki-NLP/opus-mt-zh-en") # = "中文 ➜ 英文"  # 可尝试切换为其他语言对，例如 "英文 ➜ 中文"
    results = []
    for i in text:
        if i:
            reuslt = translate_text(model, tokenizer, device,i)
            print(reuslt)
            results.append(reuslt)
    return results

def start_trans_ENtoZH(text: list[str]):
    model, tokenizer, device = load_model("Helsinki-NLP/opus-mt-en-zh") # = "中文 ➜ 英文"  # 可尝试切换为其他语言对，例如 "英文 ➜ 中文"
    results =[]
    for i in text:
        if i:
            reuslt = translate_text(model, tokenizer, device,i)
            print(reuslt)
            results.append(reuslt)
    return results


def test1():
    # 输入参数
    task = "中文 ➜ 英文"  # 可尝试切换为其他语言对，例如 "英文 ➜ 中文"
    text = "我们可以通过 HuggingFace 提供的工具高效完成翻译任务。"
    device_setting = "auto"  # 可选: "cpu", "cuda", "auto"
    precision_setting = "fp16"  # 可选: "fp32", "fp16", "int8"

    # 执行翻译任务
    try:
        translated_text, time_stats = translate_text_with_time(
            task=task,
            text=text,
            device_setting=device_setting,
            precision_setting=precision_setting,
        )
        # 输出翻译结果和阶段耗时
        print(f"\n【{task}】\n翻译结果: {translated_text}")
        print("阶段耗时统计:")
        print(f"1. 分词耗时: {time_stats[0]:.4f} 秒")
        print(f"2. 翻译耗时: {time_stats[1]:.4f} 秒")
        print(f"3. 解码耗时: {time_stats[2]:.4f} 秒")
        print(f"总翻译耗时: {sum(time_stats):.4f} 秒")

    except ValueError as e:
        print(str(e))


# ==== 示例调用 ====
if __name__ == "__main__":
   text=["你好","世界","黄河之水天上来，奔流到海不复回"]
   # zh_results = start_trans_ZHtoEN(text)
   # print(zh_results)
   # print("\n\nxxxxxxxxxx\n\n\n")
   en_results = start_trans_ENtoZH(['Hello', 'World', 'The waters of the Yellow River come up and run to the sea.'])
   print(en_results)
