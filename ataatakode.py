import requests
import json

url = "https://teamupapi.inuit.gl/AppPlayerScore"

payload = json.dumps({
  "id": "10D867FA-502E-4B55-B1A8-2191FF551627",
  "aboutAppId": "709b0a17-725c-4b97-8195-19b6a50c58cf",
  "playerId": "DAN",
  "score": 150,
  "lastDataUpdate": "2025-03-18T18:40:39.904Z"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
#teamupapi.inuit.gl

