import random

import dawg_python

from imports import *
from pars_hotels import get_prices
from get_tikcets import get_tikсets
from get_places import get_places
from weather_with_chatgpt import weather, local_food, facts
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


THIMBLE = '⚫'
but = [types.Button("Да", payload=True), types.Button("Нет", payload=False)]

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
]
answers = positive + negative

type_of_housing = [
    "отел",
    "хостел",
    "апарт",
    "дом",
    "кемпинг",
]

help = [
    'хелп',
    'что ты умеешь',
    'что ты можешь',
]

answers_to_type = negative + type_of_housing

have_tickets = ["А билеты есть?", "У вас уже есть билеты?", "Вы уже приобрели себе билеты?"]
have_housing = ["А жильё есть?", "У вас уже есть жильё?", "Вы уже забранировали сеье жильё?", "Вы уже знаете, где будете жить?"]
help_with_housing = ["Вам помочь с жильём?", "Вам помочь найти жильё?", "Вам помочь с выбором жилья?"]
help_with_tickets = ["Вам помочь с билетами?", "Вам помочь найти билеты?", "Вам помочь с выбором билетов?"]
help_with_housing_and_tickets = ["Вам почь с билетами и жильём", "Вам помочь найти билеты и жильё?", "Вам помочь с выбором жилья и билетов?"]
help_text = "Я могу сориентировать вас по ценам на билеты и жильё. Также я могу рассказать много интересного про страну: различные факты, прогноз погоды, какие места стоит посетить и какую еду попробовать. Помимо этого, я могу подсказать, что нужно с собой взять. Продолжайте работать"


@dp.request_handler(state=how.GEO)
async def main(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=how.GEO)
    try:
        geo_point = alice_request.request._raw_kwargs["nlu"]["entities"][0]["value"]
        await dp.storage.update_data(user_id, GEO=geo_point)
    except:
        return alice_request.response("Так куда вы хотите?",tts="Так куда вы хотите?")
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
        return alice_request.response("Так когда вы хотите?", tts="Так когда вы хотите приехать?")
    await dp.storage.set_state(user_id, how.BILETS)
    data = await dp.storage.get_data(user_id)
    q1 = queue.Queue()
    event1 = Event()
    q2 = queue.Queue()
    event2 = Event()
    q3 = queue.Queue()
    event3 = Event()
    t1 = Thread(target=weather,args=[data,event1,q1])
    t1.start()
    t2 = Thread(target=local_food,args=[data,event2,q2])
    t2.start()
    t3 = Thread(target=facts, args=[data, event3, q3])
    t3.start()
    await dp.storage.update_data(user_id, threads=[[event1,q1],[event2,q2],[event3,q3]])
    # task1 = asyncio.ensure_future(weather(dp,user_id))
    text = random.choice(have_tickets)
    return alice_request.response(text, buttons=but, tts=text)

@dp.request_handler(state=how.BILETS, request_type=types.RequestType.BUTTON_PRESSED)
async def Bilets(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=how.BILETS)
    await dp.storage.update_data(user_id, BILETS=alice_request.request.payload)
    await dp.storage.set_state(user_id, how.SLEEP)
    return alice_request.response(random.choice(have_housing), buttons=but)


@dp.request_handler(state=how.BILETS, commands=answers)
async def Bilets(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=how.BILETS)
    if alice_request.request.command in negative:
        alice_request.request.command = False
    elif alice_request.request.command in positive:
        alice_request.request.command = True
    await dp.storage.update_data(user_id, BILETS=alice_request.request.command)
    await dp.storage.set_state(user_id, how.SLEEP)
    return alice_request.response(random.choice(have_housing), buttons=but)

# @dp.request_handler(state=how.BILETS)
# async def Bilets(alice_request):
#     return alice_request.response("Я не совсем поняла ваш ответ, повторите ещё раз.",tts="Я не совсем поняла ваш ответ, повторите ещё раз.")


@dp.request_handler(state=how.SLEEP, request_type=types.RequestType.BUTTON_PRESSED)
async def Sleep(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=how.SLEEP)
    await dp.storage.update_data(user_id, SLEEP=alice_request.request.payload)
    await dp.storage.reset_state(user_id)
    # await dp.storage.set_state(user_id, find.TRIP)
    data = await dp.storage.get_data(user_id)
    ticket = data["BILETS"]
    hostel = data["SLEEP"]
    if ticket and hostel:
        print("END")
        return alice_request.response(await end_of_diolog(alice_request))

    elif ticket and not hostel:
        print("SECOND BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_2)
        return alice_request.response(random.choice(help_with_housing))

    elif not ticket and hostel:
        print("THIRD BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_3)
        return alice_request.response(random.choice(help_with_tickets))

    else:
        print("FIRST BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_1)
        return alice_request.response(random.choice(help_with_housing_and_tickets))


@dp.request_handler(state=how.SLEEP, commands=answers)  # Тут тоже самое
async def Sleep(alice_request):
    user_id = alice_request.session.user_id
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
        return alice_request.response(text,tts=text)

    elif ticket and not hostel:
        print("SECOND BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_2)
        return alice_request.response(random.choice(help_with_housing))

    elif not ticket and hostel:
        print("THIRD BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_3)
        return alice_request.response(random.choice(help_with_tickets))

    else:
        print("FIRST BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_1)
        return alice_request.response(random.choice(help_with_housing_and_tickets))

# @dp.request_handler(state=how.SLEEP)
# async def Sleep(alice_request):
#     return alice_request.response("Я не совсем поняла ваш ответ, повторите ещё раз.", tts="Я не совсем поняла ваш ответ, повторите ещё раз.")

@dp.request_handler(state=find.BRANCH_1, commands=answers)
async def branch_def(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=find.BRANCH_1)
    if alice_request.request.command in negative:
        return alice_request.response(await end_of_diolog(alice_request))
    await dp.storage.update_data(user_id, get_both=True)
    await dp.storage.set_state(user_id, find.APARTAMENTS)
    return alice_request.response("Какой вариант размещения вы предпочитаете? Мы можем предложить вам варианты отеля, хостела, апартаментов, гостевого дома или кемпинга",tts="Какой вариант размещения вы предпочитаете? Мы можем предложить вам варианты отеля, хостела, апартаментов, гостевого дома или кемпинга")

@dp.request_handler(state=find.BRANCH_2, commands=answers)
async def hotel(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=find.BRANCH_2)
    if alice_request.request.command in negative:
        return alice_request.response(await end_of_diolog(alice_request))
    await dp.storage.update_data(user_id, get_both=False)

    await dp.storage.set_state(user_id, find.APARTAMENTS)
    return alice_request.response("Какой вариант размещения вы предпочитаете? Мы можем предложить вам варианты отеля, хостела, апартаментов, гостевого дома или кемпинга",tts="Какой вариант размещения вы предпочитаете? Мы можем предложить вам варианты отеля, хостела, апартаментов, гостевого дома или кемпинга")

@dp.request_handler(state=find.BRANCH_3, commands=answers)
async def from_where(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=find.BRANCH_3)
    if alice_request.request.command in negative:
        return alice_request.response(await end_of_diolog(alice_request))
    await dp.storage.set_state(user_id, find.TICKETS)
    return alice_request.response("Откуда вы поедете?",tts="Откуда вы поедете?")

@dp.request_handler(state=find.APARTAMENTS, comands=answers_to_type)
async def get_apartamets(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=find.APARTAMENTS)
    t = await dp.storage.get_data(user_id)
    print(t)
    TO = t['GEO']["city"]
    if not t["get_both"]:
        if alice_request.request.command in negative:
            return alice_request.response(end_of_diolog(alice_request))
        elif "отел" in alice_request.request.command:
            return alice_request.response(await get_prices(TO, 'hotel', 'отели') + await end_of_diolog(alice_request))
        elif "хостел" in alice_request.request.command:
            return alice_request.response(await get_prices(TO, 'hostel', 'хостелы') + await end_of_diolog(alice_request))
        elif "апарт" in alice_request.request.command:
            return alice_request.response(await get_prices(TO, 'apart', 'апартаменты') + await end_of_diolog(alice_request))
        elif "дом" in alice_request.request.command:
            return alice_request.response(await get_prices(TO, 'guesthouse', 'номер в гостевом доме') + await end_of_diolog(alice_request))
        elif "кемпинг" in alice_request.request.command:
            return alice_request.response(await get_prices(TO, 'camping', 'кемпинг') + await end_of_diolog(alice_request))
    else:
        if alice_request.request.command in negative:
            return alice_request.response(end_of_diolog(alice_request))
        elif "отел" in alice_request.request.command:
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response(await get_prices(TO, 'hotel', 'отели') + "\nОткуда вы поедете")
        elif "хостел" in alice_request.request.command:
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response(await get_prices(TO, 'hostel', 'хостелы') + "\nОткуда вы поедете")
        elif "апарт" in alice_request.request.command:
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response(await get_prices(TO, 'apart', 'апартаменты') + "\nОткуда вы поедете")
        elif "дом" in alice_request.request.command:
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response(await get_prices(TO, 'guesthouse', 'номер в гостевом доме') + "\nОткуда вы поедете")
        elif "кемпинг" in alice_request.request.command:
            await dp.storage.set_state(user_id, find.TICKETS)
            return alice_request.response(await get_prices(TO, 'camping', 'кемпинг') + "\nОткуда вы поедете")

async def end_of_diolog(alice_request):
    print("ABOBA1")
    user_id = alice_request.session.user_id
    await dp.storage.set_state(user_id, find.END)
    return "\n\nВам бы хотелось узнать еще что-то про погоду, местную кухню или интересные места. Я могу помочь собрать чемодан и заодно поделиться интересными фактами об этом городе (стране)."

@dp.request_handler(state=find.END,commands=["билетик"])
async def return_again(alice_request):
    return alice_request.response("\n\nВам бы хотелось узнать еще что-то про погоду, местную кухню или интересные места. Я могу помочь собрать чемодан и заодно поделиться интересными фактами об этом городе (стране).", tts="Вам бы хотелось узнать еще что-то про погоду, местную кухню или интересные места. Я могу помочь собрать чемодан и заодно поделиться интересными фактами об этом городе (стране).")

@dp.request_handler(state=find.END)
async def end_diolog(alice_request):
    print("ABOBA2")
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, state=find.END)

    t = await dp.storage.get_data(user_id)
    TO = t['GEO']["city"]
    if alice_request.request.command in negative:
        await dp.storage.reset_state(user_id,with_data=True)
        return alice_request.response("Ну тогда была рада помочь, обращайтесь",tts="Ну тогда была рада помочь, обращайтесь",end_session=True)
    else:
        if 'погод' in alice_request.request.original_utterance:
            t["threads"][0][0].wait()
            return alice_request.response(t['threads'][0][1].get() + await end_of_diolog(alice_request))
        elif 'места' in alice_request.request.original_utterance:
            print("ABOBA3")
            return alice_request.response(await get_places(TO) + await end_of_diolog(alice_request))
        elif 'кухн' in alice_request.request.original_utterance or 'ед' in alice_request.request.original_utterance or 'местн' in alice_request.request.original_utterance:
            t["threads"][1][0].wait()
            return alice_request.response(t['threads'][1][1].get() + await end_of_diolog(alice_request))
        elif 'факт' in alice_request.request.original_utterance:
            t["threads"][2][0].wait()
            return alice_request.response(t['threads'][2][1].get() + await end_of_diolog(alice_request))
        # t["threads"][1][0].wait()
        # t['threads'][1][1].get()

@dp.request_handler(func=lambda areq: areq.session.new)
async def handle_new_session(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id)
    logging.info(f'Initialized suggests for new session!\nuser_id is {user_id!r}')
    await dp.storage.set_state(user_id, how.GEO)
    return alice_request.response('Давайте. Когда и куда вы хотите отправиться?',tts='Давайте. Когда и куда вы хотите отправиться?')


@dp.request_handler(state=find.TICKETS)
async def get_tickets(alice_request):
    if alice_request.request.nlu.entities[0].type == "YANDEX.GEO":
        user_id = alice_request.session.user_id
        await dp.storage.update_data(user_id, state=find.TICKETS)
        FROM = alice_request.request.nlu.entities[0].value

        t = await dp.storage.get_data(user_id)
        answer = await get_tikсets(t, FROM.city)
        try:
            text, button = answer
            return alice_request.response(text + await end_of_diolog(alice_request), buttons=[button])
        except:
            text = answer
            return alice_request.response(text + await end_of_diolog(alice_request))
    else:
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
    return alice_request.response("Извините, я не совсем поняла, что вы сказали, повторите ещё раз")

@dp.request_handler(commands=["я передумал","заверши"])
async def exit(alice_request):
    return alice_request.response()

if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT, loop=dp.loop)