from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
sys.path.append(os.path.abspath('..'))

from aip import AipNlp

from base.utils import img2base64, access_token
from base.utils import get_json, post_json

import json

class Image(object):

    def __init__(self, filename, regs):
        self.app_id, self.app_key, self.secret_key = regs
        self.filename = filename
        self.base64 = img2base64(filename)

    def is_same_as(self, image):
        return self.base64 == image.base64

    def find_logo(self):
        res = None
        token = access_token(url='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.app_key + '&client_secret=' + self.secret_key,
            key='access_token')
        params = {"custom_lib":True, "image":self.base64}
        url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/logo?access_token=" + token
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = json.loads(post_json(url, data=params, headers=headers))
        print(data)
        if data is not None:
            res = data.get('result')
        return res

if '__main__' == __name__:
    from config import IMAGE_REGS
    img1 = Image('mj1.jpg', IMAGE_REGS)
#    img2 = Image('mj2.jpg', IMAGE_REGS)

    print(img1.find_logo())