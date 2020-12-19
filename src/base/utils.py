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

def weekday(t=None):
    if t is None:
        t = datetime.date.today()
    d = datetime.date.weekday(t)
    if 6 == d:
        res = '日'
    else:
        res = str(d + 1)
    return res

def get_img_content(img_fn):
    res = None
    with open(img_fn, 'rb') as f:
        res = f.read()
    return res

def img2base64(img):
    return base64.b64encode(img)

def base64img(img_fn):
    res = get_img_content(img_fn)
    if res is not None:
        res = img2base64(res)
    return res

def access_token(url, key='access_token'):
    res = None
    data = json.loads(get_json(url))
    if data is not None:
        res = data.get(key)
    return res
