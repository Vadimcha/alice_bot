from itertools import groupby
from pymorphy2 import MorphAnalyzer

s = "Я хочу поехать в Дубаи"
m = s.split(" ")
items = []
for i in m:
    if i[0].isupper() == 1:
        items.append(i)

morph = MorphAnalyzer()


words = []
for i in items:
    words.append(morph.parse(i)[0])

ans = ''
for i in words:
    if i.tag.POS == 'NOUN':
        ans = i.normal_form

ans = ans[0].upper() + ans[1:]
print(ans)