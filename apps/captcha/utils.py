import random
from rest_captcha import captcha


def getsize(font, text):
    if hasattr(font, 'getoffset'):
        return tuple(
            [x + y for x, y in zip(font.getsize(text), font.getoffset(text))])
    else:
        return font.getbbox(text)[2:]


captcha.getsize = getsize


def random_char_challenge(length):
    chars = '012345689'
    ret = ''
    for i in range(length):
        ret += random.choice(chars)
    return ret.upper()
