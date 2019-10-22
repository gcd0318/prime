from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
sys.path.append(os.path.abspath('..'))

from aip import AipNlp
from config import TMP_PATH

class NLP(object):
    def __init__(self, regs):
        app_ip, api_key, secret_key = regs
        self.client = AipNlp(app_ip, api_key, secret_key)

if '__main__' == __name__:
    from config import NLP_REGS
    n = NLP(NLP_REGS)
    print(n.client.lexer('今天北京的天气'))
    print(n.client.emotion('闭嘴'))