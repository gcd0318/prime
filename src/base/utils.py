import base64
import datetime
import json
import requests
import time

def get_json(url, headers=None):
    res = None
    if headers is None:
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
    resp = requests.get(url, headers=headers)
    if 200 == resp.status_code:
        res = resp.text
    return res

def post_json(url, headers=None, data=None):
    res = None
    if headers is None:
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
    resp = requests.post(url=url, data=data, headers=headers)
    if 200 == resp.status_code:
        res = resp.text
    return res

def timestamp(t=None, fmt='%Y%m%d_%H%M%S'):
    if t is None:
        t = time.localtime()
    return time.strftime(fmt, t)

def weekday(t=None):
    if t is None:
        t = datetime.date.today()
    d = datetime.date.weekday(t)
    if 6 == d:
        res = '日'
    else:
        res = str(d + 1)
    return res

def img2base64(img_fn):
    res = None
    with open(img_fn, 'rb') as f:
        res = base64.b64encode(f.read())
    return res

def refresh_token(url, key):
    res = None
    data = json.loads(get_json(url))
    if data is not None:
        res = data.get(key)
    return res
