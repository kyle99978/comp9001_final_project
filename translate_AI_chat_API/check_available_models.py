# other links
# https://github.com/popjane/free_chatgpt_api


#######
# https://github.com/chatanywhere/GPT_API_free?tab=readme-ov-file
# https://github.com/chatanywhere/GPT_API_free?tab=readme-ov-file
#free gpt-4o，gpt-4.1  5/day；
# free deepseek-r1, deepseek-v3 30/day，
# gpt-4o-mini，gpt-3.5-turbo，gpt-4.1-mini，gpt-4.1-nano 200/day。
# Host1: https://api.chatanywhere.tech (国内中转，延时更低,Domestic transit with lower latency)
# Host2: https://api.chatanywhere.org (国外使用,Foreign use)



import http.client
import json


def get_available_models():
   conn = http.client.HTTPSConnection("api.chatanywhere.tech")
   payload = ''
   headers = {
      'Authorization': 'your_api_key'
   }
   conn.request("GET", "/v1/models", payload, headers)
   res = conn.getresponse()
   data = res.read()

   A0 = data.decode("utf-8")
   # {"object":"list",
   #  "data":[{"id":"gpt-4o-mini-2024-07-18","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"gpt-4o-mini","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"text-embedding-3-large","object":"model","created":1705953180,"owned_by":"openai"},
   #          {"id":"gpt-4.1-nano","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"gpt-3.5-turbo-1106","object":"model","created":1698959748,"owned_by":"openai"},
   #          {"id":"gpt-4.1-mini-2025-04-14","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"gpt-3.5-turbo","object":"model","created":1677610602,"owned_by":"openai"},
   #          {"id":"gpt-4o-ca","object":"model","created":1706048358,"owned_by":"ca"},
   #          {"id":"gpt-4o-mini-ca","object":"model","created":1715367049,"owned_by":"ca"},
   #          {"id":"gpt-4o","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"gpt-4o-2024-05-13","object":"model","created":1715368132,"owned_by":"openai"},
   #          {"id":"deepseek-r1","object":"model","created":1706048358,"owned_by":"ca"},
   #          {"id":"gpt-3.5-turbo-ca","object":"model","created":1706048358,"owned_by":"ca"},
   #          {"id":"text-embedding-3-small","object":"model","created":1705948997,"owned_by":"openai"},
   #          {"id":"deepseek-v3","object":"model","created":1706048358,"owned_by":"ca"},
   #          {"id":"gpt-4o-mini-2024-07-18-ca","object":"model","created":1715367049,"owned_by":"ca"},
   #          {"id":"gpt-4.1-nano-2025-04-14","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"gpt-4.1","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"gpt-4.1","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"text-embedding-ada-002","object":"model","created":1671217299,"owned_by":"openai"},
   #          {"id":"gpt-4.1-mini","object":"model","created":1715367049,"owned_by":"openai"},
   #          {"id":"gpt-3.5-turbo-0125","object":"model","created":1706048358,"owned_by":"openai"}
   #        ]
   # }

   # print(type(A0))  # 检查A1的类型，应该是字符串 <class 'str'>

   # Use json.loads() to parse JSON strings into dictionaries
   # 使用json.loads()将JSON字符串解析为字典
   A1 = json.loads(A0)  #
   # print(type(A1))
   # 验证解析后的类型是否为字典 <class 'dict'>
   # Verify that the parsed type is a dictionary <class 'dict'>

   A3 = A1['object']

   A4 = type(A1['data'])  # list
   A5 = len(A1['data'])  # 22
   A6 = A1['data'][0]
   # print(type(A6))  # <class 'dict'>

   models=[]
   for i in A1['data']:
     # print(i)
      models.append(i['id'])
   return models

if __name__ == "__main__":
   models = get_available_models()
   models.sort()
   # print(models)

# {'id': 'gpt-4o-mini-2024-07-18', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'gpt-4o-mini', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'text-embedding-3-large', 'object': 'model', 'created': 1705953180, 'owned_by': 'openai'}
# {'id': 'gpt-4.1-nano', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'gpt-3.5-turbo-1106', 'object': 'model', 'created': 1698959748, 'owned_by': 'openai'}
# {'id': 'gpt-4.1-mini-2025-04-14', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'gpt-3.5-turbo', 'object': 'model', 'created': 1677610602, 'owned_by': 'openai'}
# {'id': 'gpt-4o-ca', 'object': 'model', 'created': 1706048358, 'owned_by': 'ca'}
# {'id': 'gpt-4o-mini-ca', 'object': 'model', 'created': 1715367049, 'owned_by': 'ca'}
# {'id': 'gpt-4o', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'gpt-4o-2024-05-13', 'object': 'model', 'created': 1715368132, 'owned_by': 'openai'}
# {'id': 'deepseek-r1', 'object': 'model', 'created': 1706048358, 'owned_by': 'ca'}
# {'id': 'gpt-3.5-turbo-ca', 'object': 'model', 'created': 1706048358, 'owned_by': 'ca'}
# {'id': 'text-embedding-3-small', 'object': 'model', 'created': 1705948997, 'owned_by': 'openai'}
# {'id': 'deepseek-v3', 'object': 'model', 'created': 1706048358, 'owned_by': 'ca'}
# {'id': 'gpt-4o-mini-2024-07-18-ca', 'object': 'model', 'created': 1715367049, 'owned_by': 'ca'}
# {'id': 'gpt-4.1-nano-2025-04-14', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'gpt-4.1', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'gpt-4.1', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'text-embedding-ada-002', 'object': 'model', 'created': 1671217299, 'owned_by': 'openai'}
# {'id': 'gpt-4.1-mini', 'object': 'model', 'created': 1715367049, 'owned_by': 'openai'}
# {'id': 'gpt-3.5-turbo-0125', 'object': 'model', 'created': 1706048358, 'owned_by': 'openai'}




















