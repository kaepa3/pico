import httpget
import ujson
import env

nw = httpget.Network(env.Ssid, env.Password)

url = "https://api.openweathermap.org/data/2.5/onecall"


params = [
    "lat=35.4478",
    "lon=139.6425",
    f"appid={env.WetherAppID}",
    "units=metric",
    "lang=ja",
]
paramstr = "&".join(params)

url = url + "?" + paramstr

print("access:" + url)

rst = nw.Access(url)

if not rst[0]:
    print("error")


print(rst[1])
ret = ujson.loads(rst[1].text)
current = ret["current"]["weather"]
print(current)
