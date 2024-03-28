import requests

url = "https://api.runpod.ai/v2/faster-whisper/status/f7a3ccb4-903d-4909-8411-f62616536f4a-u1"
headers = {"accept": "application/json"}

response = requests.post(url, headers=headers)

print(response.text)