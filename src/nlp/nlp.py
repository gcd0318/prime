from aip import AipNlp

from config import TMP_PATH

class NLP(object):
    def __init__(self, app_ip, api_key, secret_key):
        self.client = AipNlp(app_ip, api_key, secret_key)

if '__main__' == __name__:
    from config import APP_ID, API_KEY, SECRET_KEY
    n = NLP(APP_ID, API_KEY, SECRET_KEY)
    print(n.client.lexer('今天北京的天气'))
    print(n.client.emotion('闭嘴'))