from bs4 import BeautifulSoup as bs
from deep_translator import GoogleTranslator
import pymorphy2
import pyshorteners
from geopy.geocoders import Nominatim
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from aioalice import types


def get_prices(event,q,TIME,location = "Пекин", tip = 'hostel', j = 'хостелы', ):
    t = time.time()
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    service = Service(executable_path="./geckodriver")
    driver = webdriver.Firefox(firefox_binary='/usr/bin/firefox-esr',service=service, options=opts)
    
    morph = pymorphy2.MorphAnalyzer()
    butyavka = morph.parse(location)[0]
    gent = butyavka.inflect({'loct'}).word.capitalize()

    lower = 1
    # location_en = translator.translate(location, src='ru', dest='en').text.lower()
    location_en = GoogleTranslator(source='ru', target='en').translate(location).lower()
    country_l = Nominatim(user_agent="GetLoc").geocode(location, language="en").address.split(",")[-1].strip().lower().split(" ")
    country = ""
    if len(country_l) == 1:
        country = country_l[0]
    else:
        for i in country_l:
            country+=i+"_"
        country = country[:-1]
    URL_TEMPLAT = f"https://ostrovok.ru/hotel/{country}/"\
        + location_en
    print(URL_TEMPLAT)
    driver.get(URL_TEMPLAT)
    time.sleep(1)
    parsed_url = urlparse(driver.current_url)
    parsed_args = parse_qs(parsed_url.query)
    url = f"https://ostrovok.ru/hotel/{country}/"\
        + location_en \
        + f"/?q={parsed_args['q'][0]}&guests=1&price=one&type_group={tip}&sort=price.asc&dates={TIME['day']}.{TIME['month']}.{TIME['year']}-{TIME['day']+1}.{TIME['month']}.{TIME['year']}&sid="\
        + parsed_args["sid"][0]
    print(url)
    driver.get(url)
    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CLASS_NAME, "hotel-wrapper")))
    r = driver.find_element(By.TAG_NAME,"html").get_attribute('innerHTML')
    soup = bs(r, "html.parser")
    prices_blocks = soup.find_all('div', class_='zen-hotelcard-rate-price-value')
    lowest_prices = []
    
    for div in prices_blocks:
        second_span = div.find_all('span')[1::2]
        for span in second_span:
            try:
                lowest_prices.append(int(span.text.replace("₽","").strip()))
            except ValueError:
                try:
                    text = span.text.replace("₽","").strip().split("\xa0")
                    num = ""
                    for i in text:
                        num+=i
                    lowest_prices.append(int(num))
                except:
                    text = span.text.replace("₽","").strip().split(",")
                    num = ""
                    for i in text:
                        num+=i
                    lowest_prices.append(int(num))
    lowest_prices.sort()
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(url)
    text = "В " + " цена за " + j + " варьируется от " + str(lowest_prices[0]) + " до " + str(lowest_prices[-1]) + " рублей за одну ночь для взрослого человека." + "\n" + "Вы можете сами посмотреть цены кликнув по кнопке: "
    but = types.Button("Отели", url=short_url)
    q.put([text,but])
    event.set()
    # await dp.storage.updtae_data(user_id, hotels=[text,but])
    print(time.time()-t)

# get_prices()
