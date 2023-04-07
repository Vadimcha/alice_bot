import openai
import calendar
import os
from dotenv import load_dotenv
from imports import Thread, Event, queue, dp
load_dotenv(".env")
t1 = os.getenv("TOKEN-1")
t2 = os.getenv("TOKEN-2")
t3 = os.getenv("TOKEN-3")
t4 = os.getenv("TOKEN-4")
t5 = os.getenv("TOKEN-5")

def weather(data,event,q):#(dp,user_id):
    openai.api_key = t1
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "кратко предоставь среднестатистическую информацию о погоде в {} в {} на основе доступных данных, не говоря о том что ты 'искуственный интелект' или 'ИИ' или 'бот'".format(data["GEO"]["city"],calendar.month_name[int(data["TIME"]["month"])])
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    except:
        q.put("Извините сервис поиска не доступен в данный момент, приносим свои извинения")
        event.set()
        return 0
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё, " + coun(completion))
    q.put(completion)
    event.set()
    # return completion

def local_food(data,event,q):
    import re
    import asyncio

    openai.api_key = t2
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "Выдай список, объёмом менее 950 символов, по номерам трёх блюд характерных для местной кухни {} с очень кратким описанием. Напиши в формате: 1. Первое блюдо 2. Второе блюдо 3. Третье блюдо   ".format(data["GEO"]["city"])
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    except:
        q.put("Извините сервис поиска не доступен в данный момент, приносим свои извинения")
        event.set()
        return 0
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x2, " + coun(completion))
    j = completion.find('1')
    completion = completion[j:]
    meals = []
    urls = []
    q.put(completion)
    # for i in range(3):
    #     f = completion.find(f"{i+1}")+2
    #     s = completion.find("-")
    #     l = completion.find(f"{i+2}") if i != 2 else len(re.findall(".",completion))-1
    #     meals.append(completion[f:s].strip())
    #     # url = Get_photos(completion[f:s].strip())
    #     url = get_photos_ya(completion[f:s].strip())[0]
    #     print(url)
    #     cur = "curl -H 'Authorization: OAuth y0_AgAAAAActKAOAAT7owAAAADgV2LrXnqbNJbVTLGOBkWB3-1OhdmazVo' -H 'Content-Type: application/json' -X POST -d '{'url': '"+url.split('&')[0]+"' }' 'https://dialogs.yandex.net/api/v1/skills/77bdccfe-350c-4bb3-a0e7-16dcbbc59681/images'"
    #     print(cur)
    #     print(os.system(cur))
    #     # urls.append()
    #     completion = completion[l:]
    # # q.put(urls)
    # q.put(meals)
    event.set()

def get_photos_ya(query):
    import requests
    from bs4 import BeautifulSoup

    url = "https://yandex.ru/images/search?text=" + query
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    images = []

    for img in soup.find_all("img"):
        images.append("https"+img["src"])
    return images[1:]
    print(images)


def Get_photos(query):
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent

    url = f'https://www.google.com/search?q={query}&tbm=isch'
    headers = {'User-Agent': UserAgent().random}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url and img_url != "/images/branding/searchlogo/1x/googlelogo_desk_heirloom_color_150x55dp.gif":
            return img_url
            # images.append(img_url)
            break
    # for i, img_url in enumerate(images):
    #     try:
    #         response = requests.get(img_url)
    #     except:
    #         continue
    #     with open(f'./images/{query}.jpg', 'wb') as f:
    #         f.write(response.content)


def facts(data,event,q):
    openai.api_key = t3
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "Сжато расскажи про три интересных факта про {} используй менее 850 символов и ответь в формате: 1. Первое место 2. Второе место, и так далее".format(data["GEO"]["city"])
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    except:
        q.put("Извините сервис поиска не доступен в данный момент, приносим свои извинения")
        event.set()
        return 0
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x3, " + coun(completion))
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()

def places(data,event,q):
    openai.api_key = t4
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "Расскажи мне про 5 самых интересных мест {} с очень кратким описанием.  Напиши не более 800 символов в формате: 1. Первое место 2. Второе место, и так далее".format(data["GEO"]["city"])
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    except:
        q.put("Извините сервис поиска не доступен в данный момент, приносим свои извинения")
        event.set()
        return 0
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x4, " + coun(completion))
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()


def chemodan(data, event, q):
    openai.api_key = t5
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "что бы ты посоветовала брать с собой в чемодан при поездке в {}. Напиши список из 15 вещей без пояснений в формате: 1. 1ый предмет 2. 2ой предмет/ и так далее Напиши не более 850 символов!".format(data["GEO"]["city"])
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    except:
        q.put("Извините сервис поиска не доступен в данный момент, приносим свои извинения")
        event.set()
        return 0
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x5, "+ coun(completion))
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()

def coun(string):
    char=0
    for i in string:
        char+=1
    return str(char)

if __name__  == "__main__":
    q5 = queue.Queue()
    event5 = Event()
    local_food({"GEO":{"city":"Москва"}, "TIME":{"month":5}},event5,q5)
# print(weather({"GEO":{"city":"Москва"}, "TIME":{"month":5}}))
