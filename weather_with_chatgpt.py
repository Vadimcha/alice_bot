import openai
import calendar

def weather(data,event,q):#(dp,user_id):
    openai.api_key = "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"
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "кратко предоставь среднестатистическую информацию о погоде в {} в {} на основе доступных данных, не говоря о том что ты 'искуственный интелект' или 'ИИ' или 'бот'".format(data["GEO"]["city"],calendar.month_name[int(data["TIME"]["month"])])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё")
    q.put(completion)
    event.set()
    # return completion

def local_food(data,event,q):
    openai.api_key = "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"
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "Выдай список по номерам трёх блюд характерных для местной кухни {} с пояснениями. Напиши менее 1024 символов в формате: 1. Первое блюдо 2. Второе блюдо 3. Третье блюдо   ".format(data["GEO"]["city"])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x2")
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()

def facts(data,event,q):
    openai.api_key = "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"
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "расскажи три интересных факта про {} в формате: 1. Первый факт 2. Второй факт 3. Третий факт".format(data["GEO"]["city"])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x3")
    j = completion.find('1')
    completion = completion[j:]
    q.put(completion)
    event.set()

# print(weather({"GEO":{"city":"Москва"}, "TIME":{"month":5}}))