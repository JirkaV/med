import os
import json

DATA_FILE = os.path.join(os.path.dirname(__file__), 'alergie.json')

data = json.load(open(DATA_FILE))
dataset = set()
for elems in data.values():
    dataset.update([x.lower() for x in elems])

def find_matches(text):
    res = []
    for elem in text.split():
        elem = elem.strip().strip(',')
        if not elem:
            continue
        if elem.lower() in dataset:
            res.append(elem)
    return res
