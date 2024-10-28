import requests

url = "https://loopnet-api.p.rapidapi.com/loopnet/lease/searchByState?page=20&pageSize=10000"

payload = { "stateId": "45", "page": 20, "pageSize": 1000 }
headers = {
	"x-rapidapi-key": "3a94f12cb2msh6c7113fad6ffd10p1675f6jsna5c6394af13e",
	"x-rapidapi-host": "loopnet-api.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

result = response.json()

