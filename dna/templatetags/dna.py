from django import template

register = template.Library()

@register.simple_tag
def highlight_changes(ref, sample):
    '''highlights changes between reference and sample'''
    assert len(ref) == len(sample)
    r, s = [], []
    for i in range(len(ref)):
        rtmp, stmp = ref[i], sample[i]
        if rtmp != stmp:
            r.append('<b>%s</b>' % rtmp)
            s.append('<b>%s</b>' % stmp)
        else:
            r.append(rtmp)
            s.append(stmp)
    return '%s -> %s' % (''.join(r), ''.join(s)) 

