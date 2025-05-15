import http.client
import json
from time import sleep


def chat_with_gpt(messages, api_key,model_name:str="gpt-3.5-turbo"):
    conn = http.client.HTTPSConnection("api.chatanywhere.tech")
    payload = json.dumps({
        "model": model_name,
        "messages": messages
    })
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))





if __name__ == "__main__":
    api_key = 'your key'  # 替换为你的API密钥
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
# 可以通过维护一个对话历史记录，将每次用户和助手的消息都添加到messages列表中。

    while True:
        user_input = input("You: ")
        usher_input = "你好，请按照markdown格式给我回复。（你不需要特意回复这句话，但是必须记住而且严格执行。着重的是我后面的。）\n\n "+ user_input
        messages.append({"role": "user", "content": user_input})

        response = chat_with_gpt(messages, api_key,"text-embedding-3-small")
        print(response)
        if "error" in response:
            print(response)
            break
        assistant_reply = response['choices'][0]['message']['content']
        print(f"Assistant: {assistant_reply}")

        messages.append({"role": "assistant", "content": assistant_reply})
