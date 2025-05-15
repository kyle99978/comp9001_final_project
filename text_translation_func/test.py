import os
import time
import torch
from transformers import MarianMTModel, MarianTokenizer
from huggingface_hub import hf_hub_download
import traceback

# 禁用 HuggingFace 符号链接警告
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "true"

# 二维数组定义语言对、模型、测试文本
# https://huggingface.co/models?sort=downloads&search=opus-mt
# Hugging Face 是一个集合了成千上万个AI模型的开源平台，你可以免费搜索、下载、调用、上传自己AI模型。
#
# Helsinki-NLP
# 最有名的东西是 Opus-MT项目（Opus Machine Translation） 这是一个多语言翻译模型集合。
# Helsinki-NLP团队用MarianMT（一个很高效的开源翻译框架）训练了上千种语言对，然后全部免费开源，而且上传到了 Hugging Face上！
#
# team bg
#主要研究方向	自然语言处理（NLP）、机器翻译（MT）、多语言模型（Multilingual Models）
# 代表成果	Tatoeba translation models、Opus-MT 系列模型
# 在Hugging Face	上传了大量他们训练的翻译模型
# 风格	轻量、开放、多语言支持特别强
# 一个研究团队（NLP研究小组），归属机构是芬兰赫尔辛基大学（University of Helsinki）


LANGUAGE_MODEL_MAPPING = [
    ["XX-英文", "xx-en", "Helsinki-NLP/opus-mt-mul-en", "白毛浮绿水，红掌拨清波"],

    # 中文到其他语言
    ["中文-英文", "zh-en", "Helsinki-NLP/opus-mt-zh-en", "白毛浮绿水，红掌拨清波"],
    ["中文-日语", "zh-ja", "Helsinki-NLP/opus-mt-tc-big-zh-ja", "白毛浮绿水，红掌拨清波"],
    # ["中文-韩文", "zh-ko", "Helsinki-NLP/opus-mt-zh-ko", "白毛浮绿水，红掌拨清波"], # 不存在
    # ["中文-俄文", "zh-ru", "Helsinki-NLP/opus-mt-zh-ru", "白毛浮绿水，红掌拨清波"], # 不存在

    # 英文到其他语言
    ["英文-中文", "en-zh", "Helsinki-NLP/opus-mt-en-zh", "White fur floats on green water, red palms row through clear waves."],
    ["英文-日文", "en-jap", "Helsinki-NLP/opus-mt-en-jap", "The red petals float on the water."],
    ["英文-韩文", "en-ko", "Helsinki-NLP/opus-mt-tc-big-en-ko", "White fur floats on green water, red palms row through clear waves."],
    ["英文-俄文", "en-ru", "Helsinki-NLP/opus-mt-en-ru", "White fur floats on green water, red palms row through clear waves."],
    ["英文-法文", "en-fr", "Helsinki-NLP/opus-mt-en-fr", "The red petals float on the water."],

    # 日文到其他语言
    ["日文-英文", "jap-en", "Helsinki-NLP/opus-mt-jap-en", "赤い花びらが水面に浮かぶ"],
    # ["日文-中文", "jap-zh", "Helsinki-NLP/opus-mt-tc-big-ja-zh", "赤い花びらが水面に浮かぶ"],
    # ["日文-韩文", "jap-ko", "Helsinki-NLP/opus-mt-jap-ko", "赤い花びらが水面に浮かぶ"],
    # ["日文-俄文", "jap-ru", "Helsinki-NLP/opus-mt-jap-ru", "赤い花びらが水面に浮かぶ"],

    # 韩文到其他语言
    ["韩文-英文", "ko-en", "Helsinki-NLP/opus-mt-ko-en", "흰 털은 녹색 물 위에 떠 있고, 붉은 손바닥은 맑은 물을 젓는다."],
    # ["韩文-中文", "ko-zh", "Helsinki-NLP/opus-mt-ko-zh", "흰 털은 녹색 물 위에 떠 있고, 붉은 손바닥은 맑은 물을 젓는다."],
    # ["韩文-日文", "ko-jap", "Helsinki-NLP/opus-mt-ko-jap", "흰 털은 녹색 물 위에 떠 있고, 붉은 손바닥은 맑은 물을 젓는다."],
    ["韩文-俄文", "ko-ru", "Helsinki-NLP/opus-mt-ko-ru", "흰 털은 녹색 물 위에 떠 있고, 붉은 손바닥은 맑은 물을 젓는다."],

    # 法文到其他语言
    ["法文-英文", "fr-en", "Helsinki-NLP/opus-mt-fr-en", "Les pétales rouges flottent sur l'eau."],
    # ["法文-中文", "fr-zh", "Helsinki-NLP/opus-mt-fr-zh", "Les pétales rouges flottent sur l'eau."],
    # ["法文-日文", "fr-jap", "Helsinki-NLP/opus-mt-fr-jap", "Les pétales rouges flottent sur l'eau."],
    # ["法文-韩文", "fr-ko", "Helsinki-NLP/opus-mt-fr-ko", "Les pétales rouges flottent sur l'eau."],
    ["法文-俄文", "fr-ru", "Helsinki-NLP/opus-mt-fr-ru", "Les pétales rouges flottent sur l'eau."],

    # 俄文到其他语言
    ["俄文-英文", "ru-en", "Helsinki-NLP/opus-mt-ru-en",
     "Белый мех плывет по зеленой воде, красные ладони гребут по чистым волнам."],
    # ["俄文-中文", "ru-zh", "Helsinki-NLP/opus-mt-ru-zh", "Белый мех плывет по зеленой воде, красные ладони гребут по чистым волнам."],
    # ["俄文-日文", "ru-jap", "Helsinki-NLP/opus-mt-ru-jap", "Белый мех плывет по зеленой воде, красные ладони гребут по чистым волнам."],
    # ["俄文-韩文", "ru-ko", "Helsinki-NLP/opus-mt-ru-ko", "Белый мех плывет по зеленой воде, красные ладони гребут по чистым волнам。"],
    ["俄文-法文", "ru-fr", "Helsinki-NLP/opus-mt-ru-fr", "Белый мех плывет по зеленой воде, красные ладони гребут по чистым волнам。"]
]


def check_model_exists(model_name: str):
    """
    检查模型是否存在于 Hugging Face Hub
    """
    try:
        hf_hub_download(repo_id=model_name, filename="config.json", cache_dir="./model_cache")
        print(f"模型【{model_name}】存在 ✅")
        return True
    except Exception:
        print(f"模型【{model_name}】不存在或不可用 ❌")
        return False


def translate_text_with_time(model_name: str, text: str,
                             device_setting: str = "auto",
                             precision_setting: str = "fp32"):
    """
    使用指定的翻译任务和输入文本进行翻译，并统计阶段时间。

    参数:
    ------
    model_name : str
        使用的模型名称（Hugging Face 模型路径）。
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
        - list: 包含各阶段时间统计 [分词耗时, 翻译耗时, 解码耗时]。
    """
    # 确认设备
    if device_setting == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = device_setting
    print(f"当前设备: {device}")

    # 如果是 CPU，强制使用 fp32
    if device == "cpu" and precision_setting != "fp32":
        print(f"⚠️ CPU 不支持 {precision_setting} 模式，自动回退至 fp32。")
        precision_setting = "fp32"

    # 加载模型和分词器
    print("正在加载模型，请稍候...")
    model = None
    tokenizer = None
    try:
        if precision_setting == "fp16" and device == "cuda":
            model = MarianMTModel.from_pretrained(model_name, torch_dtype=torch.float16, cache_dir="./model_cache")
        else:
            model = MarianMTModel.from_pretrained(model_name, cache_dir="./model_cache")
        tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir="./model_cache")
    except Exception as e:
        print(f"加载模型失败 ⚠️: {e}")
        return None, None

    model = model.to(device)

    # 翻译阶段计时
    inputs = tokenizer([text], return_tensors="pt", padding=True).to(device)

    # 翻译文本
    try:
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    except Exception as e:
        print(f"翻译失败 ⚠️: {e}")
        return None, None

    return translated_text, []


def test_translation_models(device_setting="auto", precision_setting="fp32"):
    """
    测试所有翻译模型是否正常运行，并输出其翻译结果与统计。

    参数:
    ------
    device_setting : str, optional
        测试所用的设备（"auto", "cpu", "cuda"）。
    precision_setting : str, optional
        模型精度（"fp32", "fp16", "int8"）。
    """
    print(f"开始测试所有翻译模型...")
    print(f"设备设置: {device_setting}, 精度设置: {precision_setting}\n")

    for lang_pair in LANGUAGE_MODEL_MAPPING:
        lang, lang_id, model_name, sample_text = lang_pair
        print(f"正在验证语言对任务: {lang} ({lang_id})")
        print(f"模型名称: {model_name}")

        # 验证模型是否存在
        if not check_model_exists(model_name):
            continue

        print(f"测试输入: {sample_text}")

        try:
            translated_text, _ = translate_text_with_time(
                model_name=model_name,
                text=sample_text,
                device_setting=device_setting,
                precision_setting=precision_setting,
            )

            if translated_text:
                print(f"翻译成功 ✅: {translated_text}\n")
            else:
                print(f"翻译失败 ❌\n")

        except Exception as e:
            print(f"测试失败，错误原因: {e}\n")
            traceback.print_exc()

    print("所有模型测试完成！")


# 执行测试脚本
if __name__ == "__main__":
    # 示例设置
    device_setting = "auto"  # 可选: "cpu", "cuda", "auto"
    precision_setting = "fp32"  # 可选: "fp32", "fp16", "int8"

    # 调用测试函数
    test_translation_models(device_setting=device_setting, precision_setting=precision_setting)

    test_translation_models(device_setting="cpu", precision_setting="int8")
    test_translation_models(device_setting="cpu", precision_setting="fp16")
    test_translation_models(device_setting="cpu", precision_setting="fp32")

    test_translation_models(device_setting="cuda", precision_setting="int8")
    test_translation_models(device_setting="cuda", precision_setting="fp16")
    test_translation_models(device_setting="cuda", precision_setting="fp32")
