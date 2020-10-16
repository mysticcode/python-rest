import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE+"hellow/tim/10")
response1 = requests.put(
    BASE+"video/10", {"name": "test", "views": 100, "likes": 10})

input()
response = requests.get(BASE+"video/10")
print(response.json())

response2 = requests.delete(BASE+"video/10")
print(response2)

response = requests.get(BASE+"video/1")
print(response.json())
