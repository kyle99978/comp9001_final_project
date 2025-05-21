import requests

# no api， read README file
# 创建Google Cloud项目：
#
# 访问Google Cloud Console，并登录你的Google账号。
# 点击“选择项目”按钮，然后点击“新建项目”。
# 输入项目名称并选择一个结算账号，然后点击“创建”。
# 启用Cloud Translation API：
#
# 在Google Cloud Console中，导航到“API和服务” > “启用API和服务”。
# 搜索“Cloud Translation API”，然后点击“启用”。
# 创建API密钥：
#
# 在“API和服务” > “凭据”页面，点击“创建凭据”按钮，然后选择“API密钥”。
# 复制生成的API密钥


# if no api， read README file
# Create a Google Cloud project:
# Create an API key.
# Access the Google Cloud Console and sign in to your Google account.
# Click the "Select Project" button and then click "New Project".
# Enter a project name and select a billing account, then click Create.
# Enable the Cloud Translation API:
# Create an API key.
# In the Google Cloud Console, navigate to "APIs and Services" > "Enable APIs and Services".
# Search for "Cloud Translation API" and click Enable.
# Create an API key:
# Create an API key.
# On the "APIs and Services" > "Credentials" page, click the "Create Credentials" button, and then select "API KeyAPI Key".
# Copy the generated API key





def translate_with_google(text, target_lang='en', source_lang='auto'):
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': text,
        'target': target_lang,
        'source': source_lang,
        'key': 'YOUR_API_KEY'  # replace with your Google Cloud API key
    }

    response = requests.post(url, params=params)
    if response.status_code == 200:
        result = response.json()
        return result['data']['translations'][0]['translatedText']
    else:
        return f"Error: {response.status_code}, {response.text}"


if __name__ == "__main__":
    text_to_translate = "你好，世界！"
    translated_text = translate_with_google(text_to_translate, target_lang='en')
    print(f"Translated text: {translated_text}")
