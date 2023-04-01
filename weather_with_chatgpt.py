import openai
import calendar
import os
from dotenv import load_dotenv
load_dotenv("../.env")
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
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=850)["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё")
    q.put(completion)
    event.set()
    # return completion

def local_food(data,event,q):
    openai.api_key = t2
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "Выдай список по номерам трёх блюд характерных для местной кухни {} с очень кратким описанием. Напиши менее 950 символов в формате: 1. Первое блюдо 2. Второе блюдо 3. Третье блюдо   ".format(data["GEO"]["city"])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=850)["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x2")
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()

def facts(data,event,q):
    openai.api_key = t3
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "Сжато расскажи про три интересных факта про {} используй менее 850 символов и ответь в формате: 1. Первое место 2. Второе место, и так далее".format(data["GEO"]["city"])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=850)["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x3")
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()

def places(data,event,q):
    openai.api_key = t4
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "Расскажи мне про 5 самых интересных мест {} с очень кратким описанием.  Напиши не более 850 символов в формате: 1. Первое место 2. Второе место, и так далее".format(data["GEO"]["city"])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=850)["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x4")
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()


def chemodan(data, event, q):
    openai.api_key = t5
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "что бы ты посоветовала брать с собой в чемодан при поездке в {}. Напиши список из 15 вещей без пояснений в формате: 1. 1ый предмет 2. 2ой предмет/ и так далее Напиши не более 850 символов!".format(data["GEO"]["city"])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=850)["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x5")
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()

# print(weather({"GEO":{"city":"Москва"}, "TIME":{"month":5}}))