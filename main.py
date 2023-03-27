from imports import *
from pars_hotels import get_prices
from get_tikcets import get_tikcets

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

answers_to_type = negative + type_of_housing

@dp.request_handler(state=how.GEO)
async def main(alice_request):
    user_id = alice_request.session.user_id
    try:
        geo_point = alice_request.request._raw_kwargs["nlu"]["entities"][0]["value"]
        await dp.storage.update_data(user_id, GEO=geo_point)
    except:
        return alice_request.response("Так куда вы хотите?")
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
        return alice_request.response("Так когда вы хотите?")
    await dp.storage.set_state(user_id, how.BILETS)
    return alice_request.response("А билеты есть?", buttons=but)


@dp.request_handler(state=how.BILETS, request_type=types.RequestType.BUTTON_PRESSED)
async def Bilets(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, BILETS=alice_request.request.payload)
    await dp.storage.set_state(user_id, how.SLEEP)
    return alice_request.response("А ночлег есть?", buttons=but)


@dp.request_handler(state=how.BILETS, commands=answers)
async def Bilets(alice_request):
    user_id = alice_request.session.user_id
    if alice_request.request.command in negative:
        alice_request.request.command = False
    elif alice_request.request.command in positive:
        alice_request.request.command = True
    await dp.storage.update_data(user_id, BILETS=alice_request.request.command)
    await dp.storage.set_state(user_id, how.SLEEP)
    return alice_request.response("А ночлег есть?", buttons=but)

@dp.request_handler(state=how.BILETS)
async def Bilets(alice_request):
    return alice_request.response("Я не совсем поняла ваш ответ, повторите ещё раз.")


@dp.request_handler(state=how.SLEEP, request_type=types.RequestType.BUTTON_PRESSED)
async def Sleep(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id, SLEEP=alice_request.request.payload)
    await dp.storage.reset_state(user_id)
    await dp.storage.set_state(user_id, find.TRIP)
    data = await dp.storage.get_data(user_id)
    return alice_request.response("ок.")


@dp.request_handler(state=how.SLEEP, commands=answers)  # Тут тоже самое
async def Sleep(alice_request):
    user_id = alice_request.session.user_id
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
        return alice_request.response(await end_of_diolog(alice_request))

    elif ticket and not hostel:
        print("SECOND BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_2)
        return alice_request.response("Вам помочь найти жильё?")

    elif not ticket and hostel:
        print("THIRD BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_3)
        return alice_request.response("Вам помочь найти билеты?")

    else:
        print("FIRST BRANCH")
        await dp.storage.set_state(user_id, find.BRANCH_1)
        return alice_request.response("Вам помочь найти билеты и жильё?")

    #return alice_request.response("")

@dp.request_handler(state=how.SLEEP)
async def Sleep(alice_request):
    return alice_request.response("Я не совсем поняла ваш ответ, повторите ещё раз.")


@dp.request_handler(state=find.BRANCH_2, commands=answers)
async def branch_def(alice_request):
    user_id = alice_request.session.user_id
    if alice_request.request.command in negative:
        return alice_request.response(await end_of_diolog(alice_request))
    await dp.storage.set_state(user_id, find.APARTAMENTS)
    return alice_request.response("Какой вариант размещения вы предпочитаете? Мы можем предложить вам варианты отеля, хостела, апартаментов, гостевого дома или кемпинга")

@dp.request_handler(state=find.BRANCH_3, commands=answers)
async def branch_def(alice_request):
    user_id = alice_request.session.user_id
    if alice_request.request.command in negative:
        return alice_request.response(await end_of_diolog(alice_request))
    await dp.storage.set_state(user_id, find.TICKETS)
    return alice_request.response("Откуда вы поедете")

@dp.request_handler(state=find.APARTAMENTS, comands=answers_to_type)
async def get_apartamets(alice_request):
    print("ABOBA")
    user_id = alice_request.session.user_id
    t = await dp.storage.get_data(user_id)
    TO = t['GEO']["city"]

    if alice_request.request.command in negative:
        return alice_request.response(end_of_diolog())
    elif "отел" in alice_request.request.command:
        return alice_request.response(await get_prices(TO, 'hotel', 'отели'))
    elif "хостел" in alice_request.request.command:
        return alice_request.response(await get_prices(TO, 'hostel', 'хостелы'))
    elif "апарт" in alice_request.request.command:
        return alice_request.response(await get_prices(TO, 'apart', 'апартаменты'))
    elif "дом" in alice_request.request.command:
        return alice_request.response(await get_prices(TO, 'guesthouse', 'номер в гостевом доме'))
    elif "кемпинг" in alice_request.request.command:
        return alice_request.response(await get_prices(TO, 'camping', 'кемпинг'))

@dp.request_handler(func=lambda areq: areq.session.new)
async def handle_new_session(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.update_data(user_id)
    logging.info(f'Initialized suggests for new session!\nuser_id is {user_id!r}')
    await dp.storage.set_state(user_id, how.GEO)
    return alice_request.response('Давайте. Когда и куда вы хотите отправиться?')

@dp.request_handler(state=find.TICKETS, func=lambda areq: areq.request.nlu.entities[0].type == "YANDEX.GEO")
async def get_tickets(alice_request):

    user_id = alice_request.session.user_id
    FROM = alice_request.request.nlu.entities[0].value

    t = await dp.storage.get_data(user_id)
    answer = await get_tikcets(t,FROM.city)

    try:
        text,button = answer
        return alice_request.response(text,buttons=[button])
    except:
        text = answer
        return alice_request.response(text)
    # return alice_request.response(f"Он хочет уехать из {FROM.city} {t['TIME']['day']}.{t['TIME']['month']}.{(t['TIME']['year'] if 'year' in t['TIME'] else '2023')} в {t['GEO']['city']}")


async def end_of_diolog(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.set_state(user_id, find.END)
    return "Вам бы хотелось о чем-нибудь ещё узнать? Я могу рассказать про погоду, достопримечательности и местную кухню. Также я могу помочь собрать чемодан и заодно поделиться интересными фактами об этом городе (стране)."

@dp.request_handler(state=find.END, commands=answers)
async def end_diolog(alice_request):
    if alice_request.request.command in positive:
        return alice_request.response("Это прекрасно, вот только пошел отсюда, я еще не умею это делать")
    else:
        return alice_request.response("Ну тогда была рада помочь, обращайтесь")




# @dp.request_handler()
# async def main(alice_request):
#     return alice_request.response()

if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT, loop=dp.loop)