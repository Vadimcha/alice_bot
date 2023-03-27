import requests
import json
import pyshorteners
from aioalice import types

url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
# url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates?currency=rub&origin={}&destination={}&departure_at={}&sorting=price&token=1f680fc9e416a09d5b858fb66716097d"
get_iatas = "https://www.travelpayouts.com/widgets_suggest_params?q=из {} в {}"

digits = [1,2,3,4,5,6,7,8,9]

async def get_tikсets(data, city):
    iatas = requests.get(get_iatas.format(city,data["GEO"]["city"])).json()
    origin = iatas["origin"]["iata"]
    destination = iatas["destination"]["iata"]
    month = "0{}".format(data["TIME"]["month"]) if data["TIME"]["month"] in digits else data["TIME"]["month"]
    day = "0{}".format(data["TIME"]["day"]) if data["TIME"]["day"] in digits else data["TIME"]["day"]
    try:
        response = requests.get(url, params={"currency":"rub","origin":origin,"destination":destination,"departure_at":f"{data['TIME']['year']}-{month}-{day}","sorting":"price","token":"1f680fc9e416a09d5b858fb66716097d"}).json()["data"][0]
        but = types.Button("билетик", url=pyshorteners.Shortener().tinyurl.short('aviasales.ru'+response['link']))
        return f"Я нашел билет на {response['departure_at'][0:10]} в {response['departure_at'][11:19]} GMT{response['departure_at'][20:25]}\nза {response['price']} можетe посмотреть сами кликнув по кнопке\n",but
    except IndexError:
        return "Не получилось найти билеты для вас"
    except Exception as e:
        print(e)
        return "что то пошло не так"