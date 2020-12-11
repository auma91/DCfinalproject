import requests, json
zip = 80134
weatherapikey = "6545ce0d4b8726f11fee3867ee16ebf8"

url = "http://api.openweathermap.org/data/2.5/weather?zip={},us&appid={}".format(zip, weatherapikey)
response = requests.get(url)
data = response.json()
lon = data['coord']['lon']
lat = data['coord']['lat']
url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(lat, lon, "current,daily,minutely,alerts", weatherapikey)
response = requests.get(url)
data = response.json()
print(len(data["hourly"]))
hourlydata = data["hourly"][:12]
rain= False
for i in hourlydata:
	print(i)
	for j in i["weather"]:
		if j["main"].lower() == "rain":
			rain = True
			break
	if rain:
		break
