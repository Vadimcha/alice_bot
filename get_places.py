from imports import *
import requests
from bs4 import BeautifulSoup as bs
from deep_translator import GoogleTranslator
import pymorphy2
import pyshorteners

async def get_places(location = "москва"):
    location = GoogleTranslator(source='ru', target='en').translate(location).lower()
    print(location)
    # location = translator.translate(location, src='ru', dest='en').text.lower()

    URL_TEMPLAT = "https://experience.tripster.ru/experience/"+location
    r = requests.get(URL_TEMPLAT)
    soup = bs(r.text, "html.parser")

    # находим все элементы списка
    items = soup.select(".exp-snippet-list .exp-list-item-wrapper")
    answer = "Вот что я нашла: \n"
    # проходимся по каждому элементу и достаем текст ссылки и цену
    sch = 0
    for item in items:
        if sch >= 5:
            break
        title = item.select_one(".title").text
        price = item.select_one(".price-current").text
        dscr = item.select_one(".tagline").text
        answer += f"{title}\n{dscr}\n Цена: {price}\n\n"
        sch += 1

    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(URL_TEMPLAT)
    return answer + "\n Также вы можете сами посмотреть на сайте " + short_url