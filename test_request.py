import requests

param = dict(typeid=2436)

resp = requests.get("https://api.evemarketer.com/ec/marketstat/json", param)
# print(resp.text)

data = resp.json()
print(data)