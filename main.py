from flask import Flask
from flask import request
from itertools import groupby
from pymorphy2 import MorphAnalyzer
import json

app = Flask(__name__)


def get_city(s): # Получает из фразы название если оно там есть
    m = s.split(" ")
    items = []
    for i in m:
        if i[0].isupper() == 1:
            items.append(i)

    morph = MorphAnalyzer()

    words = []
    for i in items:
        words.append(morph.parse(i)[0])

    for i in words:
        if i.tag.POS == 'NOUN':
            ans = i.normal_form

    ans = ans[0].upper() + ans[1:]
    print(ans)
    return ans


@app.route('/post', methods=['POST'])
def main():
    ## Создаем ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    diolog(response, request.json)
    return json.dumps(response)

def diolog(res,req):
    if not req['request']['original_utterance'] and req["session"]["message_id"] == 0:
        res['response']['text'] = 'Давайте. Когда и куда вы хотите отправиться?'
    else:
        res['response']['text'] = get_city(req['request']['original_utterance'])

if __name__ == '__main__':
    app.run()

