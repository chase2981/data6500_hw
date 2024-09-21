import requests
import json

word_key = 'word'
score_key = 'score'

example_url = 'https://api.datamuse.com/words?ml=utah'

req = requests.get(example_url)
txt = req.text
# print(txt)

lst_dct = json.loads(txt)

for dct in lst_dct:
    if dct[word_key] == 'uva':
        print('uva!!! ', dct[score_key])

