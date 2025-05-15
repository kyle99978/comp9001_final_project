import customtkinter as ctk
import tkinter as tk

from sympy.strategies.util import basic_fns

# window
index_win = tk.Tk()
index_win.withdraw()

############################# frame1 #########################################
frame1 = None
# textbox
textbox = None
textbox_scrollbar_vertical = None


############################# frame2 #########################################
frame2 = None
# 创建 StringVars
model_languages_main = {
    "Deutsch (German)": "DE",
    "English (English)": "EN",
    "Français (French)": "FR",
    "日本語 (Japanese)": "JA",
    "中文 (Chinese)": "ZH",
    "粵語 (Cantonese)": "YUE",
    "ALL (all languages)": "ALL",
    "None": "NONE",
}
selected_option_1 = ctk.StringVar(value="None")
selected_option_2 = ctk.StringVar(value="None")

option_menu_1 = None
label_arrows = None
option_menu_2 = None

tabview = None

frame2_1 = None
frame2_2 = None
frame2_3 = None

Model_tab_scroll_frame = None
Audio_tab_scroll_frame = None
Theme_tab_scroll_frame = None

Model_radio_var = tk.StringVar(value="tiny")  # 控制变量
model_rb=[]  # radiobuttons
model_names = [ "whisper.tiny",
                "whisper.base",
                "whisper.small",
                "whisper.medium",
                "whisper.large-v2",
                "whisper.large-v3",
                ]

Audio_radio_var = tk.StringVar(value="MP3 File")
audio_btn=[]
audio_radio_options =  [  "MP3 File",  "WAV File", "MP4 File",
                          "System Voice", "Microphone_1",
                          "Edge", "Chrome",
                        ]

theme_app = ["System", "Blue", "Dark", "DarkBlue", "Light", "Green"]



bottom_button_values = [" Start ", " Stop ", " End ", " Hide "]

frame3 = None


# arrow
label_arrows=None


# buttons
segemented_button = None
button_more=None




model="tiny"
audio_source ="System voice"
running_status=0, # 0,1=start,2=stop,,3=end

all_status={"input_language": None,
            "output_language": None,
            "model": None,
}


model_languages_all = {
    "af": "南非荷兰语 (Afrikaans)",
    "am": "阿姆哈拉语 (Amharic)",
    "ar": "阿拉伯语 (Arabic)",
    "as": "阿萨姆语 (Assamese)",
    "az": "阿塞拜疆语 (Azerbaijani)",
    "ba": "巴什基尔语 (Bashkir)",
    "be": "白俄罗斯语 (Belarusian)",
    "bg": "保加利亚语 (Bulgarian)",
    "bn": "孟加拉语 (Bengali)",
    "bo": "藏语 (Tibetan)",
    "br": "布列塔尼语 (Breton)",
    "bs": "波斯尼亚语 (Bosnian)",
    "ca": "加泰罗尼亚语 (Catalan)",
    "cs": "捷克语 (Czech)",
    "cy": "威尔士语 (Welsh)",
    "da": "丹麦语 (Danish)",
    "de": "德语 (German)",
    "el": "希腊语 (Greek)",
    "en": "英语 (English)",
    "es": "西班牙语 (Spanish)",
    "et": "爱沙尼亚语 (Estonian)",
    "eu": "巴斯克语 (Basque)",
    "fa": "波斯语 (Persian)",
    "fi": "芬兰语 (Finnish)",
    "fo": "法罗语 (Faroese)",
    "fr": "法语 (French)",
    "gl": "加利西亚语 (Galician)",
    "gu": "古吉拉特语 (Gujarati)",
    "ha": "豪萨语 (Hausa)",
    "haw": "夏威夷语 (Hawaiian)",
    "he": "希伯来语 (Hebrew)",
    "hi": "印地语 (Hindi)",
    "hr": "克罗地亚语 (Croatian)",
    "ht": "海地克里奥尔语 (Haitian Creole)",
    "hu": "匈牙利语 (Hungarian)",
    "hy": "亚美尼亚语 (Armenian)",
    "id": "印度尼西亚语 (Indonesian)",
    "is": "冰岛语 (Icelandic)",
    "it": "意大利语 (Italian)",
    "ja": "日语 (Japanese)",
    "jw": "爪哇语 (Javanese)",
    "ka": "格鲁吉亚语 (Georgian)",
    "kk": "哈萨克语 (Kazakh)",
    "km": "高棉语 (Khmer)",
    "kn": "卡纳达语 (Kannada)",
    "ko": "韩语 (Korean)",
    "la": "拉丁语 (Latin)",
    "lb": "卢森堡语 (Luxembourgish)",
    "ln": "林加拉语 (Lingala)",
    "lo": "老挝语 (Lao)",
    "lt": "立陶宛语 (Lithuanian)",
    "lv": "拉脱维亚语 (Latvian)",
    "mg": "马达加斯加语 (Malagasy)",
    "mi": "毛利语 (Maori)",
    "mk": "马其顿语 (Macedonian)",
    "ml": "马拉雅拉姆语 (Malayalam)",
    "mn": "蒙古语 (Mongolian)",
    "mr": "马拉地语 (Marathi)",
    "ms": "马来语 (Malay)",
    "mt": "马耳他语 (Maltese)",
    "my": "缅甸语 (Burmese)",
    "ne": "尼泊尔语 (Nepali)",
    "nl": "荷兰语 (Dutch)",
    "nn": "挪威尼诺斯克语 (Norwegian Nynorsk)",
    "no": "挪威语 (Norwegian)",
    "oc": "奥克语 (Occitan)",
    "pa": "旁遮普语 (Punjabi)",
    "pl": "波兰语 (Polish)",
    "ps": "普什图语 (Pashto)",
    "pt": "葡萄牙语 (Portuguese)",
    "ro": "罗马尼亚语 (Romanian)",
    "ru": "俄语 (Russian)",
    "sa": "梵语 (Sanskrit)",
    "sd": "信德语 (Sindhi)",
    "si": "僧伽罗语 (Sinhalese)",
    "sk": "斯洛伐克语 (Slovak)",
    "sl": "斯洛文尼亚语 (Slovenian)",
    "sn": "修纳语 (Shona)",
    "so": "索马里语 (Somali)",
    "sq": "阿尔巴尼亚语 (Albanian)",
    "sr": "塞尔维亚语 (Serbian)",
    "su": "巽他语 (Sundanese)",
    "sv": "瑞典语 (Swedish)",
    "sw": "斯瓦希里语 (Swahili)",
    "ta": "泰米尔语 (Tamil)",
    "te": "泰卢固语 (Telugu)",
    "tg": "塔吉克语 (Tajik)",
    "th": "泰语 (Thai)",
    "tk": "土库曼语 (Turkmen)",
    "tl": "塔加洛语 (Tagalog)",
    "tr": "土耳其语 (Turkish)",
    "tt": "鞑靼语 (Tatar)",
    "uk": "乌克兰语 (Ukrainian)",
    "ur": "乌尔都语 (Urdu)",
    "uz": "乌兹别克语 (Uzbek)",
    "vi": "越南语 (Vietnamese)",
    "yi": "意第绪语 (Yiddish)",
    "yo": "约鲁巴语 (Yoruba)",
    "zh": "中文 (Chinese)",
    "yue": "粤语 (Cantonese)"
}





