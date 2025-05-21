import requests


def translate_text(text, target_lang='EN'):
    url = "https://api-free.deepl.com/v2/translate"
    target_lang = target_lang
    params = {
        'auth_key': 'your key',  # Replace it with your  API key
        'text': text,
        'target_lang': target_lang
    }

    response = requests.post(url, data=params)
    if response.status_code == 200:  # 状态码是200，表示请求成功。 A status code of 200 indicates that the request was successful.
        result = response.json()
        # 如果请求成功，代码将响应转换为JSON格式，并提取翻译结果。
        # If the request is successful, the code converts the response to JSON and extracts the translation.
        
        # result['translations'][0]['text'] 获取翻译后的文本并返回。 # Get the translated text and return it.
        # A1 = result
        # A2 = result['translations']
        # A3 = result['translations'][0]
        A4 = result['translations'][0]['text']

        # print(type(A1), type(A2), type(A3), type(A4))
        # <class 'dict'> <class 'list'> <class 'dict'> <class 'str'>

        # print(len(A1), len(A2), len(A3), len(A4))
        # # 1 1 2 13
        #
        # print(A1, A2, A3, A4)
        # {'translations': [{'detected_source_language': 'ZH', 'text': 'Hello, world!'}]}
        # [{'detected_source_language': 'ZH', 'text': 'Hello, world!'}]
        # {'detected_source_language': 'ZH', 'text': 'Hello, world!'}
        # Hello, world!

        return A4
    else:
        return f"Error: {response.status_code}, {response.text}"



def init_deepl_session(auth_key: str, target_lang='EN'):
    """初始化 DeepL API 会话参数"""
    """Initialising DeepL API session parameters""""
    return {
        'url': "https://api-free.deepl.com/v2/translate",
        'auth_key': auth_key,
        'target_lang': target_lang
    }

def translate_text2(text: str, session_data: dict):
    """翻译文本，使用预初始化的 session_data"""
    """Translate text, using pre-initialised session_data""""
    params = {
        'auth_key': session_data['auth_key'],
        'text': text,
        'target_lang': session_data['target_lang']
    }

    response = requests.post(session_data['url'], data=params)
    if response.status_code == 200:
        result = response.json()
        return result['translations'][0]['text']
    else:
        return f"Error: {response.status_code}, {response.text}"


if __name__ == "__main__":
    text_to_translate = "你"
    translated_text = translate_text(text_to_translate, target_lang='EN')
    print(f"Translated text: {translated_text}")
