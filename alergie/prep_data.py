import json

alergie = {}

with open('alergie.txt') as f:
    for line in f:
        if 'kupina' in line:
            cislo_skupiny = line.strip().split()[-1].rstrip('/')
            continue
        elems = [x.strip() for x in line.split(',') if x.strip()]
        if not elems:
            continue
        try:
            alergie[cislo_skupiny].extend(elems)
        except KeyError:
            alergie[cislo_skupiny] = elems

with open('alergie.json', 'w') as out:
    json.dump(alergie, out)