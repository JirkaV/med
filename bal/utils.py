import datetime

def rc2datum(rc_):
    d = rc_[:6]
    if d[2] == '5':
        d = d[:2] + '0' + d[3:]
    if d[2] == '6':
        d = d[:2] + '1' + d[3:]
    # cizinci: d = d+50
    if d[4] in ['5', '6', '7']:
        d = d[:4] + str(int(d[4])-5) + d[5:]
    try:
        datum = datetime.datetime.strptime(d, '%y%m%d').date()
    except ValueError:
        print '[!] Chyba v RC: [%s]' % rc_
        raise
    return datum
