import requests

url = "https://teamupapi.inuit.gl/AppPlayerScore/709b0a17-725c-4b97-8195-19b6a50c58cf"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
#teamupapi.inuit.gl