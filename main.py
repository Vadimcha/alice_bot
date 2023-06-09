import random

from imports import *
from pars_hotels import get_prices
from get_tikcets import get_tikcets
from weather_with_chatgpt import weather, local_food, facts, places, chemodan
class how(Helper):
    mode = HelperMode.snake_case
    GEO = Item()
    TIME = Item()
    BILETS = Item()
    SLEEP = Item()


class find(Helper):

    mode = HelperMode.snake_case
    TRIP = Item()
    BRANCH_1 = Item()
    BRANCH_2 = Item()
    BRANCH_3 = Item()
    APARTAMENTS = Item()
    TICKETS = Item()
    HELP = Item()
    END = Item()

    def reset_help(self):
        self.HELP = Item()


but = [types.Button("Да", payload=True), types.Button("Нет", payload=False)]
help_buttons = [types.Button("Помощь", payload="help_pls"), types.Button("Что ты умеешь?", payload="whaaaa?")]

positive = [
    "да",
    "разумеется",
    "ага",
    "давай",
    "конечно",
    "несомненно",
    "плюс",
    "так точно",
    "угу",
    "ну давай",
    "ну да",
    "а как же",
    "а то как же",
    "йес",
    "есть",
    "есть",
    "yes",
    "ес",
]
negative = [
    "и в помине нет",
    "не имеется",
    "не имеется в наличии",
    "отсутствует",
    "недостаёт",
    "и в помине не было",
    "нет",
    "нету",
    "неа",
    "ноу",
    "нет, конечно",
    "нетушки",
    "ничуть",
    "ничего подобного",
    "no",
]
answers = positive + negative

type_of_housing = [
    "отел",
    "хостел",
    "апарт",
    "дом",
    "кемпинг",
]

what_can_u_do = [
    'что ты умеешь',
    'что ты можешь',
    ]
help = [
    'хелп',
    'помощь',
]



answers_to_type = negative + type_of_housing

have_tickets = ["А билеты есть?", "У вас уже есть билеты?", "Вы уже приобрели себе билеты?"]
have_housing = ["А жильё есть?", "У вас уже есть жильё?", "Вы уже забронировали себе жильё?", "Вы уже знаете, где будете жить?"]
help_with_housing = ["Вам помочь с жильём?", "Вам помочь найти жильё?", "Вам помочь с выбором жилья?"]
help_with_tickets = ["Вам помочь с билетами?", "Вам помочь найти билеты?", "Вам помочь с выбором билетов?"]
help_with_housing_and_tickets = ["Вам помочь с билетами и жильём", "Вам помочь найти билеты и жильё?", "Вам помочь с выбором жилья и билетов?"]
help_text = ["Я могу сориентировать вас по ценам на билеты и жильё. Также я могу рассказать много интересного про страну: различные факты, прогноз погоды, какие места стоит посетить и какую еду попробовать. \
              Помимо этого, я могу подсказать, что нужно с собой взять. \n \nЧтобы продолжить работать ответьте на предыдущий вопрос", \
              "Я могу помочь вам узнать цены на билеты и жильё, а также поделиться множеством интересных фактов о стране, рассказать о прогнозе погоды, порекомендовать места для посещения и блюда, которые стоит попробовать. \
                Кроме того, я могу советовать, что необходимо взять с собой."
]

phrases = ["жиль", "номер", "апартамент", "квартир", "гостиниц", "аренд"]



@dp.request_handler()
async def ping(alice_request):
    if alice_request.request.original_utterance == "ping":
        return alice_request.response("200")
    else:
        raise SkipHandler

@dp.request_handler(state=find.TICKETS, commands=help)
@dp.request_handler(state=find.TICKETS, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=how.GEO, commands=help)
@dp.request_handler(state=how.GEO, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=how.BILETS, commands=help)
@dp.request_handler(state=how.BILETS, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=how.SLEEP, commands=help)
@dp.request_handler(state=how.SLEEP, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_1, commands=help)
@dp.request_handler(state=find.BRANCH_1, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_2, commands=help)
@dp.request_handler(state=find.BRANCH_2, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_3, commands=help)
@dp.request_handler(state=find.BRANCH_3, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.END, commands=help)
@dp.request_handler(state=find.END, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.APARTAMENTS, commands=help)
@dp.request_handler(state=find.APARTAMENTS, request_type=types.RequestType.BUTTON_PRESSED)
async def helping(alice_request):
    user_id = alice_request.session.user_id
    data = await dp.storage.get_data(user_id)
    if alice_request.request.type == types.RequestType.BUTTON_PRESSED:
        if alice_request.request.payload == "help_pls": 
            print("Запросил помощь")
            text, but = h(data,alice_request)
            return alice_request.response(text,buttons=but)
        else:
            raise SkipHandler
    else:
        print("Запросил помощь")
        text, but = h(data,alice_request)
        return alice_request.response(text,buttons=but)

def h(data,alice_request):
    he = '\nЕсли вы застряли на одном месте: скажите "начать заново" и пробуйте снова'
    match (data['state']):
        case 'geo':
            return "Вам нужно ответить на вопрос куда вы хотите поехать"+he,help_buttons
        case 'tickets':
            return "Вам нужно написать откуда вы уезжаете"+he,help_buttons
        case 'bilets':
            return "Вам нужно ответить на вопрос есть ли у вас билеты"+he,but+help_buttons
        case 'sleep':
            return "Вам нужно ответить на вопрос есть ли у вас жилье"+he,but+help_buttons
        case 'branch_1':
            return "Вам нужно ответить нужна ли вам помощь с поиском жилья и билетов"+he,but+help_buttons
        case 'branch_2':
            return "Вам нужно ответить нужна ли вам помошь с поиском жилья"+he,but+help_buttons
        case 'branch_3':
            return "Вам нужно ответить нужна ли вам помошь с поиском билетов"+he,but+help_buttons
        case 'end':
            return "Вам нужно выбрать одну из тем: погода, интересные факты, интересные места, собрать чемодан, местная кухня, варианты жилья, и сказать об этом мне"+he,help_buttons
        case 'apartaments':
            return "Вам нужно выбрать один из вариантов размещения: отель, хостел, апартаменты, гостевой дом или кемпинг"+he,help_buttons
        case _:
            return "",help_buttons



@dp.request_handler(state=find.TICKETS, commands=what_can_u_do)
@dp.request_handler(state=find.TICKETS, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=how.GEO, commands=what_can_u_do)
@dp.request_handler(state=how.GEO, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=how.BILETS, commands=what_can_u_do)
@dp.request_handler(state=how.BILETS, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=how.SLEEP, commands=what_can_u_do)
@dp.request_handler(state=how.SLEEP, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_1, commands=what_can_u_do)
@dp.request_handler(state=find.BRANCH_1, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_2, commands=what_can_u_do)
@dp.request_handler(state=find.BRANCH_2, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_3, commands=what_can_u_do)
@dp.request_handler(state=find.BRANCH_3, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.END, commands=what_can_u_do)
@dp.request_handler(state=find.END, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.APARTAMENTS, commands=what_can_u_do)
@dp.request_handler(state=find.APARTAMENTS, request_type=types.RequestType.BUTTON_PRESSED)
async def what_can_i_do(alice_request):
    user_id = alice_request.session.user_id
    if alice_request.request.type == types.RequestType.BUTTON_PRESSED:
        if alice_request.request.payload == "whaaaa?":
            print("Что я могу")
            return alice_request.response(random.choice(help_text),buttons=help_buttons)
        else:
            raise SkipHandler
    else:
        print("Что я могу")
        return alice_request.response(random.choice(help_text),buttons=help_buttons)


@dp.request_handler(state=find.TICKETS, commands=["начать заново", "заново", "повторить"])
@dp.request_handler(state=how.GEO, commands=["начать заново", "заново", "повторить"])
@dp.request_handler(state=how.BILETS, commands=["начать заново", "заново", "повторить"])
@dp.request_handler(state=how.SLEEP, commands=["начать заново", "заново", "повторить"])
@dp.request_handler(state=find.BRANCH_1, commands=["начать заново", "заново", "повторить"])
@dp.request_handler(state=find.BRANCH_2, commands=["начать заново", "заново", "повторить"])
@dp.request_handler(state=find.BRANCH_3, commands=["начать заново", "заново", "повторить"])
@dp.request_handler(state=find.END, commands=["начать заново", "заново", "повторить"])
@dp.request_handler(state=find.APARTAMENTS, commands=["начать заново", "заново", "повторить"])
async def repeat(alice_request):
    print("Перезапуск")
    await dp.storage.reset_state(user_id=alice_request.session.user_id, with_data=True)
    return await handle_new_session(alice_request)

@dp.request_handler(state=how.GEO)
async def main(alice_request):
    print("Получение места и даты выезда")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=how.GEO)    
    try:
        geo_point = alice_request.request._raw_kwargs["nlu"]["entities"][0]["value"]
        print(geo_point)
        if "city" not in geo_point.keys() and "country" in geo_point.keys():
            return alice_request.response("Укажите город, а не страну.\nОтветом отправьте полную строку с местом и датой прибытия",buttons=help_buttons)
        elif "city" not in geo_point.keys() and "country" not in geo_point.keys():
            return alice_request.response("Я не смогла определить город, попробуйте ещё раз.\nОтветом отправьте полную строку с местом и датой прибытия",buttons=help_buttons)
        await dp.storage.update_data(user_id, GEO=geo_point)
    except Exception as e:
        print(e)
        return alice_request.response("Так куда вы хотите?\nОтветом отправьте полную строку с местом и датой прибытия",tts="Так куда вы хотите? Ответом отправьте полную строку с местом и датой прибытия",buttons=help_buttons)
    try:
        time = list(filter(lambda type: type['type'] == 'YANDEX.DATETIME', alice_request.request._raw_kwargs["nlu"]["entities"]))[0]["value"]
        time["year"] = datetime.now().strftime("%Y")
        if "через" in alice_request.request.original_utterance:
            now = datetime.now()
            if 'day' in time:
                days = timedelta(time['day'])
                in_days = now + days
                time = {
                    'day': in_days.strftime("%d"),
                    'month': in_days.strftime("%m"),
                    'year': in_days.strftime("%Y"),
                }

            elif 'month' in time:
                days = timedelta(time['month'] * 30)
                in_days = now + days
                time = {
                    'day': in_days.strftime("%d"),
                    'month': in_days.strftime("%m"),
                    'year': in_days.strftime("%Y"),
                }

        await dp.storage.update_data(user_id, TIME=time)
    except IndexError:
        return alice_request.response("Так когда вы хотите?\nОтветом отправьте полную строку с точкой прибытия и временем", tts="Так когда вы хотите приехать? Ответом Отправьте полную строку с точкой прибытия и временем",buttons=help_buttons)
    await dp.storage.set_state(user_id, how.BILETS)
    await dp.storage.update_data(user_id, state=how.BILETS)
    data = await dp.storage.get_data(user_id)
    q1 = queue.Queue()
    event1 = Event()
    q2 = queue.Queue()
    event2 = Event()
    q3 = queue.Queue()
    event3 = Event()
    q4 = queue.Queue()
    event4 = Event()
    q5 = queue.Queue()
    event5 = Event()
    t1 = Thread(target=weather, args=[data, event1, q1])
    t1.start()
    t2 = Thread(target=local_food, args=[data, event2, q2])
    t2.start()
    t3 = Thread(target=facts, args=[data, event3, q3])
    t3.start()
    t4 = Thread(target=places, args=[data, event4, q4])
    t4.start()
    t5 = Thread(target=chemodan, args=[data, event5, q5])
    t5.start()
    await dp.storage.update_data(user_id, threads=[[event1, q1], [event2, q2], [event3, q3], [event4, q4], [event5, q5]])
    # task1 = asyncio.ensure_future(weather(dp,user_id))
    text = random.choice(have_tickets)
    return alice_request.response(text, buttons=but+help_buttons, tts=text)

@dp.request_handler(state=how.BILETS, request_type=types.RequestType.BUTTON_PRESSED)
async def Bilets(alice_request):
    print("Есть ли у пользователя билеты?")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    await dp.storage.update_data(user_id, BILETS=alice_request.request.payload)
    await dp.storage.set_state(user_id, how.SLEEP)
    await dp.storage.update_data(user_id, state=how.SLEEP)
    return alice_request.response(random.choice(have_housing), buttons=but+help_buttons)


@dp.request_handler(state=how.BILETS, commands=answers)
async def Bilets(alice_request):
    print("Есть ли у пользователя билеты?")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    if alice_request.request.command in negative:
        alice_request.request.command = False
    elif alice_request.request.command in positive:
        alice_request.request.command = True
    await dp.storage.update_data(user_id, BILETS=alice_request.request.command)
    await dp.storage.set_state(user_id, how.SLEEP)
    await dp.storage.update_data(user_id, state=how.SLEEP)
    return alice_request.response(random.choice(have_housing), buttons=but+help_buttons)

# @dp.request_handler(state=how.BILETS)
# async def Bilets(alice_request):
#     return alice_request.response("Я не совсем поняла ваш ответ, повторите ещё раз.",tts="Я не совсем поняла ваш ответ, повторите ещё раз.")


@dp.request_handler(state=how.SLEEP, request_type=types.RequestType.BUTTON_PRESSED)
async def Sleep(alice_request):
    print("Есть ли у пользователя жилье?")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    await dp.storage.update_data(user_id, SLEEP=alice_request.request.payload)
    await dp.storage.reset_state(user_id)
    # await dp.storage.set_state(user_id, find.TRIP)
    data = await dp.storage.get_data(user_id)
    ticket = data["BILETS"]
    hostel = data["SLEEP"]
    if ticket and hostel:
        return alice_request.response(await end_of_diolog(alice_request),buttons=help_buttons)

    elif ticket and not hostel:
        print("SECOND BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_2)
        await dp.storage.update_data(user_id, state=find.BRANCH_2)
        return alice_request.response(random.choice(help_with_housing),buttons=but+help_buttons)

    elif not ticket and hostel:
        print("THIRD BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_3)
        await dp.storage.update_data(user_id, state=find.BRANCH_3)
        return alice_request.response(random.choice(help_with_tickets),buttons=but+help_buttons)

    else:
        print("FIRST BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_1)
        await dp.storage.update_data(user_id, state=find.BRANCH_1)
        return alice_request.response(random.choice(help_with_housing_and_tickets),buttons=but+help_buttons)


@dp.request_handler(state=how.SLEEP, commands=answers)  # Тут тоже самое
async def Sleep(alice_request):
    print("Есть ли у пользователя жилье?")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    await dp.storage.update_data(user_id, state=how.SLEEP)
    if alice_request.request.command in negative:
        alice_request.request.command = False
    elif alice_request.request.command in positive:
        alice_request.request.command = True
    await dp.storage.update_data(user_id, SLEEP=alice_request.request.command)
    # await dp.storage.set_state(user_id, find.TRIP)
    await dp.storage.reset_state(user_id)
    data = await dp.storage.get_data(user_id)
    ticket = data["BILETS"]
    hostel = data["SLEEP"]
    if ticket and hostel:
        print("END")
        text = await end_of_diolog(alice_request)
        return alice_request.response(text,tts=text,buttons=but+help_buttons)

    elif ticket and not hostel:
        print("SECOND BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_2)
        await dp.storage.update_data(user_id, state=find.BRANCH_2)
        return alice_request.response(random.choice(help_with_housing),buttons=but+help_buttons)

    elif not ticket and hostel:
        print("THIRD BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_3)
        await dp.storage.update_data(user_id, state=find.BRANCH_3)
        return alice_request.response(random.choice(help_with_tickets),buttons=but+help_buttons)

    else:
        print("FIRST BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_1)
        await dp.storage.update_data(user_id, state=find.BRANCH_1)
        return alice_request.response(random.choice(help_with_housing_and_tickets),buttons=but+help_buttons)

# @dp.request_handler(state=how.SLEEP)
# async def Sleep(alice_request):
#     return alice_request.response("Я не совсем поняла ваш ответ, повторите ещё раз.", tts="Я не совсем поняла ваш ответ, повторите ещё раз.")

@dp.request_handler(state=find.BRANCH_1, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_1, commands=answers)
async def branch_def(alice_request):
    print("Ветка, когда нет ничгео")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    
    if alice_request.request.type == types.RequestType.BUTTON_PRESSED:
        if alice_request.request.payload == True:
            await dp.storage.update_data(user_id, get_both=True)
            await dp.storage.set_state(user_id, find.APARTAMENTS)
            await dp.storage.update_data(user_id, state=find.APARTAMENTS)
            return alice_request.response("Какой вариант размещения вы предпочитаете? Мы можем предложить вам отели, хостелы, апартаменты, гостевые дома или кемпинги",tts="Какой вариант размещения вы предпочитаете? Мы можем предложить вам отели, хостелы, апартаменты, гостевые дома или кемпинги",buttons=help_buttons)
        else:
            return alice_request.response(await end_of_diolog(alice_request),buttons=help_buttons)
    else:
        if alice_request.request.command in negative:
            return alice_request.response(await end_of_diolog(alice_request),buttons=help_buttons)
        await dp.storage.update_data(user_id, get_both=True)
        await dp.storage.set_state(user_id, find.APARTAMENTS)
        await dp.storage.update_data(user_id, state=find.APARTAMENTS)
        return alice_request.response("Какой вариант размещения вы предпочитаете? Мы можем предложить вам отели, хостелы, апартаменты, гостевые дома или кемпинги",tts="Какой вариант размещения вы предпочитаете? Мы можем предложить вам отели, хостелы, апартаменты, гостевые дома или кемпинги",buttons=help_buttons)

@dp.request_handler(state=find.BRANCH_2, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_2, commands=answers)
async def hotel(alice_request):
    print("Ветка, когда у нас нет жилья")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    if alice_request.request.type == types.RequestType.BUTTON_PRESSED:
        if alice_request.request.payload == True:
            await dp.storage.update_data(user_id, get_both=False)

            await dp.storage.set_state(user_id, find.APARTAMENTS)
            await dp.storage.update_data(user_id, state=find.APARTAMENTS)
            return alice_request.response("Какой вариант размещения вы предпочитаете? Мы можем предложить вам отели, хостелы, апартаменты, гостевые дома или кемпинги",tts="Какой вариант размещения вы предпочитаете? Мы можем предложить вам отели, хостелы, апартаменты, гостевые дома или кемпинги",buttons=help_buttons)
        else:
            return alice_request.response(await end_of_diolog(alice_request),buttons=help_buttons)
    else:
        if alice_request.request.command in negative:
            return alice_request.response(await end_of_diolog(alice_request),buttons=help_buttons)
        await dp.storage.update_data(user_id, get_both=False)

        await dp.storage.set_state(user_id, find.APARTAMENTS)
        await dp.storage.update_data(user_id, state=find.APARTAMENTS)
        return alice_request.response("Какой вариант размещения вы предпочитаете? Мы можем предложить вам отели, хостелы, апартаменты, гостевые дома или кемпинги",tts="Какой вариант размещения вы предпочитаете? Мы можем предложить вам отели, хостелы, апартаменты, гостевые дома или кемпинги",buttons=help_buttons)

@dp.request_handler(state=find.BRANCH_3, request_type=types.RequestType.BUTTON_PRESSED)
@dp.request_handler(state=find.BRANCH_3, commands=answers)
async def from_where(alice_request):
    print("Ветка когда у нас нет билетов")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    
    if alice_request.request.type == types.RequestType.BUTTON_PRESSED:
        if alice_request.request.payload == True:
            await dp.storage.set_state(user_id, find.TICKETS)
            await dp.storage.update_data(user_id, state=find.TICKETS)
            return alice_request.response("Откуда вы поедете?",tts="Откуда вы поедете?",buttons=help_buttons)
        else:
            return alice_request.response(await end_of_diolog(alice_request))
    else:
        if alice_request.request.command in negative:
            return alice_request.response(await end_of_diolog(alice_request))
        await dp.storage.set_state(user_id, find.TICKETS)
        await dp.storage.update_data(user_id, state=find.TICKETS)
        return alice_request.response("Откуда вы поедете?",tts="Откуда вы поедете?",buttons=help_buttons)

@dp.request_handler(state=find.APARTAMENTS, comands=answers_to_type)
async def get_apartamets(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    print("Получение информации о жилье")
    
    t = await dp.storage.get_data(user_id)
    q6 = queue.Queue()
    event6 = Event()
    
    print(t)
    TO = t['GEO']["city"]
    if not t["get_both"]:
        for i in alice_request.request.nlu.tokens:
            if i in negative:
                return alice_request.response(end_of_diolog(alice_request),buttons=help_buttons)
        if "отел" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'hotel', 'отели'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + await end_of_diolog(alice_request),buttons=help_buttons)
        elif "хостел" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'hostel', 'хостелы'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав : 'Расскажи про варианты жилья'" + await end_of_diolog(alice_request),buttons=help_buttons)
        elif "апарт" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'apart', 'апартаменты'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + await end_of_diolog(alice_request),buttons=help_buttons)
        elif "дом" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'guesthouse', 'номер в гостевом доме'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + await end_of_diolog(alice_request),buttons=help_buttons)
        elif "кемпинг" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'camping', 'кемпинг'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + await end_of_diolog(alice_request),buttons=help_buttons)
        else:
            raise SkipHandler
    else:
        for i in alice_request.request.nlu.tokens:
            if i in negative:
                return alice_request.response(end_of_diolog(alice_request),buttons=help_buttons)
        if "отел" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'hotel', 'отели'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + "\nОткуда вы поедете?",buttons=help_buttons)
        elif "хостел" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'hostel', 'хостелы'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + "\nОткуда вы поедете?",buttons=help_buttons)
        elif "апарт" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'apart', 'апартаменты'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + "\nОткуда вы поедете?",buttons=help_buttons)
        elif "дом" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'guesthouse', 'номер в гостевом доме'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + "\nОткуда вы поедете?",buttons=help_buttons)
        elif "кемпинг" in alice_request.request.command:
            t6 = Thread(target=get_prices, args=[event6, q6,t["TIME"],TO, 'camping', 'кемпинг'])
            t6.start()
            await dp.storage.update_data(user_id,threads=t["threads"] + [[event6,q6]])
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response("Я отправила ваш запрос, но к сожалению вам придётся подождать, спустя минуту спросите меня про номер сказав: 'Расскажи про варианты жилья'" + "\nОткуда вы поедете?",buttons=help_buttons)
        else:
            raise SkipHandler

async def end_of_diolog(alice_request):
    print("Вопрос о доп информации")
    user_id = alice_request.session.user_id
    await dp.storage.set_state(user_id, find.END)
    await dp.storage.update_data(user_id, state=find.END)
    return "\n\nВам бы хотелось узнать еще что-то про погоду, местную кухню или интересные места. Я могу помочь собрать чемодан и заодно поделиться интересными фактами об этом городе."

@dp.request_handler(state=find.END,commands=["билетик"])
async def return_again(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0)
    print("Вопрос о доп информации")
    return alice_request.response("\n\nВам бы хотелось узнать еще что-то про погоду, местную кухню или интересные места. Я могу помочь собрать чемодан и заодно поделиться интересными фактами об этом городе.", tts="Вам бы хотелось узнать еще что-то про погоду, местную кухню или интересные места. Я могу помочь собрать чемодан и заодно поделиться интересными фактами об этом городе (стране).",buttons=help_buttons)

@dp.request_handler(state=find.END)
async def end_diolog(alice_request):
    print("Дополнительная информация")
    user_id = alice_request.session.user_id

    print(alice_request.request.command)
    t = await dp.storage.get_data(user_id)
    print(t)
    TO = t['GEO']["city"]
    for i in alice_request.request.nlu.tokens:
        print(i)
        if i in negative:
            await dp.storage.reset_state(user_id,with_data=True)
            return alice_request.response_big_image("Я была рада помочь, обращайтесь!", "213044/d4027ad94ee6dc17e228","Пока :c","Я была рада помочь, обращайтесь!",tts="Я была рада помочь, обращайтесь!", end_session=True)
    if 'погод' in alice_request.request.command:
        await dp.storage.update_data(user_id, SCHET=0)
        print("Поинтересовался местной погодой")
        if "weather" in t.keys():
            text = t["weather"]
        else:
            if t["threads"][0][0].is_set():
                text = t['threads'][0][1].get()
                await dp.storage.update_data(user_id, weather=text)
            else:
                return alice_request.response("Извините. Ответ не готов, повторите попытку позже, спросив про эту же категорию",buttons=help_buttons)
        return alice_request.response(text + await end_of_diolog(alice_request),buttons=help_buttons)
    elif 'места' in alice_request.request.command:
        await dp.storage.update_data(user_id, SCHET=0)
        print("Поинтересовался интересными местами")
        if "places" in t.keys():
            text = t["places"]
        else:
            if t["threads"][3][0].is_set():
                text = t['threads'][3][1].get()
                await dp.storage.update_data(user_id, places=text)
            else:
                return alice_request.response("Извините. Ответ не готов, повторите попытку позже, спросив про эту же категорию",buttons=help_buttons)
        return alice_request.response(text + await end_of_diolog(alice_request),buttons=help_buttons)
    elif 'кухн' in alice_request.request.command or 'ед' in alice_request.request.command or 'местн' in alice_request.request.command:
        await dp.storage.update_data(user_id, SCHET=0)
        print("Поинтересовался местной кухней")
        if "cuisine" in t.keys():
            text = t["cuisine"]
        else:
            if t["threads"][1][0].is_set():
                text = t['threads'][1][1].get()
                # meals = t['threads'][1][1].get()
                # for meal in meals:
                #     import requests
                #     import os
                #     from fake_useragent import UserAgent
                #     headers = {
                #                 'Authorization': "OAuth y0_AgAAAAActKAOAAT7owAAAADgV2LrXnqbNJbVTLGOBkWB3-1OhdmazVo", 
                #                'Content-Type': 'application/json',
                #                'User-Agent': UserAgent().random}
                #     # data = requests.post("https://dialogs.yandex.net/api/v1/skills/77bdccfe-350c-4bb3-a0e7-16dcbbc59681/images",headers=headers, data={"url": meal}).json()
                #     cur = f"curl   -H 'Authorization: OAuth y0_AgAAAAActKAOAAT7owAAAADgV2LrXnqbNJbVTLGOBkWB3-1OhdmazVo'   -H 'Content-Type: application/json'   -X POST   -d '{ 'url': {meal} }'   'https://dialogs.yandex.net/api/v1/skills/77bdccfe-350c-4bb3-a0e7-16dcbbc59681/images'"
                #     print(os.system(cur))
                    # print(data)
                    # print(await dp.upload_image(meal))
                await dp.storage.update_data(user_id, cuisine=text)
            else:
                return alice_request.response("Извините. Ответ не готов, повторите попытку позже, спросив про эту же категорию",buttons=help_buttons)
        return alice_request.response( text + await end_of_diolog(alice_request),buttons=help_buttons)
    elif 'факт' in alice_request.request.command:
        await dp.storage.update_data(user_id, SCHET=0)
        print("Поинтересовался интересными фактами")
        if "facts" in t.keys():
            text = t["facts"]
        else:
            if t["threads"][2][0].is_set():
                text = t['threads'][2][1].get()
                await dp.storage.update_data(user_id, facts=text)
            else:
                return alice_request.response("Извините. Ответ не готов, повторите попытку позже, спросив про эту же категорию",buttons=help_buttons)
        return alice_request.response( text + await end_of_diolog(alice_request),buttons=help_buttons)
    elif 'чемод' in alice_request.request.command or 'собр' in alice_request.request.command:
        await dp.storage.update_data(user_id, SCHET=0)
        print("Захотел собрать чемодан")
        if "suitcase" in t.keys():
            text = t["suitcase"]
        else:
            if t["threads"][4][0].is_set():
                text = t['threads'][4][1].get()
                await dp.storage.update_data(user_id, suitcase=text)
            else:
                return alice_request.response("Извините. Ответ не готов, повторите попытку позже, спросив про эту же категорию",buttons=help_buttons)
        return alice_request.response( text + await end_of_diolog(alice_request),buttons=help_buttons)
    else:
        for phrase in phrases:
            if phrase in alice_request.request.command:
                if "book" in t.keys():
                    text = t["book"]
                else:
                    if t["threads"][5][0].is_set():
                        text = t['threads'][5][1].get()
                        await dp.storage.update_data(user_id, book=text)
                    else:
                        if not t["SLEEP"]:
                            return alice_request.response("Извините. Ответ не готов, повторите попытку позже, спросив снова про варианты жилья",buttons=help_buttons)
                        else:
                            return alice_request.response("Вы не запрашивали помощь с жильём", buttons=help_buttons)
                return alice_request.response( text[0] + await end_of_diolog(alice_request),buttons=[text[1]]+help_buttons)
        raise SkipHandler
        # t["threads"][1][0].wait()
        # t['threads'][1][1].get()

@dp.request_handler(func=lambda areq: areq.session.new)
async def handle_new_session(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SCHET=0,state="geo")
    logging.info(f'Initialized suggests for new session!\nuser_id is {user_id!r}')
    print("Словил новую маслину")
    await dp.storage.set_state(user_id, how.GEO)
    text = 'Навык "Волшебный чемоданчик" поможет вам найти жилье, выбрать билеты, собрать вещи и узнать больше о том месте,куда вы направляетесь.\nВы можете задать вопрос: "Что ты умеешь?" для подробного описания функционала или сказать "Помощь" для того чтобы узнать, что делать дальше. Также вы всегда можете начать с самого начала с помощью фразы "Начать заново".\nТак куда и когда вы желаете поехать?'
    return alice_request.response_big_image(text,"1652229/d3e37933f0afdac28458", "Волшебный чемоданчик", text, tts=text, buttons = help_buttons)


@dp.request_handler(state=find.TICKETS)
async def get_tickets(alice_request):
    user_id = alice_request.session.user_id
    print("Получение информации о билетах")
    try:
        if alice_request.request.nlu.entities[0].type == "YANDEX.GEO": #ОБРАБОТАТЬ ЕСЛИ НИХРЕНА НЕ ПОЛУЧИЛ!!!!
            await dp.storage.update_data(user_id, SCHET=0)
            FROM = alice_request.request.nlu.entities[0].value

            t = await dp.storage.get_data(user_id)
            answer = await get_tikcets(t, FROM.city)
            try:
                text, button = answer
                return alice_request.response(text + await end_of_diolog(alice_request), buttons=[button]+help_buttons)
            except:
                text = answer
                return alice_request.response(text + await end_of_diolog(alice_request),buttons=help_buttons)
        else:
            raise SkipHandler
    except:
        raise SkipHandler   
    # return alice_request.response(f"Он хочет уехать из {FROM.city} {t['TIME']['day']}.{t['TIME']['month']}.{(t['TIME']['year'] if 'year' in t['TIME'] else '2023')} в {t['GEO']['city']}")


@dp.request_handler(state=find.TICKETS)
@dp.request_handler(state=how.GEO)
@dp.request_handler(state=how.BILETS)
@dp.request_handler(state=how.SLEEP)
@dp.request_handler(state=find.BRANCH_1)
@dp.request_handler(state=find.BRANCH_2)
@dp.request_handler(state=find.BRANCH_3)
@dp.request_handler(state=find.END)
@dp.request_handler(state=find.APARTAMENTS)
async def dont_understood(alice_request):
    user_id = alice_request.session.user_id
    print("Ничерта не поняла")
    data = await dp.storage.get_data(user_id)
    if data["SCHET"] == 0:
        await dp.storage.update_data(user_id, SCHET=1)
        return alice_request.response("Извините, я не совсем поняла, что вы сказали, повторите ещё раз",buttons=help_buttons)
    elif data["SCHET"] == 1:
        await dp.storage.update_data(user_id, SCHET=2)
        match (data['state']):
            case 'geo':
                return alice_request.response("абоба тут никого не будет",buttons=help_buttons)
            case 'tickets':
                return alice_request.response("Я снова вас не поняла. Пожалуйста, корректно введите место отъезда",buttons=help_buttons)
            case 'bilets':
                return alice_request.response("Я снова вас не поняла. Пожалуйста, ответьте да или нет, на вопрос есть ли у вас билеты",buttons=but+help_buttons)
            case 'sleep':
                return alice_request.response("Я снова вас не поняла. Пожалуйста, ответьте да или нет, на вопрос нужна ли вам помощь с билетами",buttons=but+help_buttons)
            case 'branch_1':
                return alice_request.response("Я снова вас не поняла. Пожалуйста, ответьте да или нет",buttons=but+help_buttons)
            case 'branch_2':
                return alice_request.response("Я снова вас не поняла. Пожалуйста, ответьте да или нет",buttons=but+help_buttons)
            case 'branch_3':
                return alice_request.response("Я снова вас не поняла. Пожалуйста, ответьте да или нет",buttons=but+help_buttons)
            case 'end':
                return alice_request.response("Я снова вас не поняла. Пожалуйста, скажите 'Нет' или напишите одну из тем: погода, интересные факты, интересные места, собрать чемодан, местная кухня, варианты жилья",buttons=help_buttons)
            case 'apartaments':
                return alice_request.response("Я снова вас не поняла. Пожалуйста, выберете один из вариантов размещения: отель, хостел, апартаменты, гостевой дом или кемпинг",buttons=help_buttons)
    else:
        if hasattr(alice_request.meta.interfaces, "screen"):
            return alice_request.response("Извините, но я совсем вас не понимаю, попробуйте написать текстом",buttons=help_buttons)
        else:
            return alice_request.response("Извините, но я совсем вас не понимаю, попробуйте открыть приложение на устройстве с экраном и написать текстом",buttons=help_buttons)


@dp.request_handler(commands=["я передумал","заверши"])
async def exit(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.reset_state(user_id,with_data=True)
    return alice_request.response_big_image("Я была рада помочь, обращайтесь!", "213044/d4027ad94ee6dc17e228","Пока :c","Я была рада помочь, обращайтесь!",tts="Я была рада помочь, обращайтесь!", end_session=True)

if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT, loop=dp.loop) #, ssl_context=ssl_context)