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

def places(data,event,q):
    openai.api_key = "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"
    # data = await dp.storage.get_data(user_id)
    print(data)
    prompt = "Выдай список интерсных мест для посещения в {} без предисловия и лишнего текста".format(data["GEO"]["city"])
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])["choices"][0]["message"]["content"]
    # await dp.storage.update_data(user_id,weather=completion)
    print("я всё x2")
    q.put(completion)
    event.set()

# print(weather({"GEO":{"city":"Москва"}, "TIME":{"month":5}}))