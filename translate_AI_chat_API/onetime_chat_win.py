import http.client
import json

conn = http.client.HTTPSConnection("api.chatanywhere.tech")
payload = json.dumps({
   "model": "gpt-3.5-turbo",
   "messages": [
      {
         "role": "system",
         "content": "You are a helpful assistant."
      },
      {
         "role": "user",
         "content": "我上一次问了你什么问题!"
      }
   ]
})
headers = {
   'Authorization': 'your key',
   'Content-Type': 'application/json'
}
conn.request("POST", "/v1/chat/completions", payload, headers)
res = conn.getresponse()
data = res.read()

A0 = data.decode("utf-8")
# print(type(A0))  <class 'str'>

A1 = json.loads(A0)
# print(type(A1))  <class 'dict'>

for key, value in A1.items():
    print(key, ":", value)

print(A1['choices'][0]['message']['content'])
