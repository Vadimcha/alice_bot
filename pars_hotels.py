from imports import *
import requests
from bs4 import BeautifulSoup as bs
from deep_translator import GoogleTranslator
import pymorphy2
import pyshorteners


async def get_prices(location = "москва", tip = 'guesthouse', j = 'хостелы'):
    morph = pymorphy2.MorphAnalyzer()
    butyavka = morph.parse(location)[0]
    gent = butyavka.inflect({'loct'}).word.capitalize()

    lower = 1
    # location_en = translator.translate(location, src='ru', dest='en').text.lower()
    location_en = GoogleTranslator(source='ru', target='en').translate(location).lower()


    URL_TEMPLAT = "https://ostrovok.ru/hotel/russia/" + \
                  location_en + \
                  "/?q=5580&dates=" + \
                  "&guests=1&price=one&type_group=" + \
                  tip + \
                  "&sort=price" + \
                  (".asc" if lower else "") + \
                  "&sid=b0ba9f80-0ca3-4951-a4f5-9140ea6d4624"
    r = requests.get(URL_TEMPLAT)
    soup = bs(r.text, "html.parser")
    prices_blocks = soup.find_all('div', class_='zen-hotelcard-rate-price-value')
    lowest_prices = []
    for div in prices_blocks:
        second_span = div.find_all('span')[1::2]
        for span in second_span:
            lowest_prices.append(int(span.text[:len(span.text) - 1]))

    lowest_prices.sort()
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(URL_TEMPLAT)
    return "В " + gent + " цена за " + j + " варьируется от " + str(lowest_prices[0]) + " до " + str(lowest_prices[-1]) + " рублей за одну ночь для взрослого человека." + "\n" + "Вы можете сами посмотреть цены на сайте: " + short_url