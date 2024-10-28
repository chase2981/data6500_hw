import requests

url = "https://loopnet-api.p.rapidapi.com/loopnet/lease/searchByBoundingBox"

payload = { "boundingBox": [-112.1659909, 41.999537, -111.4015759, 41.369149] }
headers = {
	"x-rapidapi-key": "3a94f12cb2msh6c7113fad6ffd10p1675f6jsna5c6394af13e",
	"x-rapidapi-host": "loopnet-api.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())