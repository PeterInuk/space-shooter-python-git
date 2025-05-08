import requests
name = input()
r = requests.get(f"http://127.0.0.1:5000/Shooter?name={name}")
print(r)
print(r.text)