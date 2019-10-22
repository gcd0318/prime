from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
sys.path.append(os.path.abspath('..'))

from aip import AipNlp

from base.utils import img2base64
from base.utils import get_json, post_json

import json

class Image(object):

    def __init__(self, filename, regs):
        self.app_id, self.app_key, self.secret_key = regs
        self.filename = filename
        self.base64 = img2base64(filename)

    def __dict__(self):
        return {"image": self.base64.decode('utf-8'), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"}

    def is_same_as(self, image):
        return self.base64 == image.base64


    def refresh_token(self):
        res = None

        url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.app_key + '&client_secret=' + self.secret_key
        data = json.loads(get_json(url))
        if data is not None:
            res = data.get('access_token')
        return res

    def compare(self, aface):
        res = -1
        params = json.dumps(
            [
                self.__dict__(),
                aface.__dict__()
            ]
        )
        url = "https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=" + self.refresh_token()
        headers = {'Content-Type': 'application/json'}
        data = json.loads(post_json(url, data=params, headers=headers))
        if data is not None:
            error_code = data.get('error_code')
            error_msg = data.get('error_msg')
            result = data.get('result')
            if (0 == error_code) and ('SUCCESS' == error_msg):
                res = result.get('score')
        return res

if '__main__' == __name__:
    from config import IMAGE_REGS
    img1 = Image('mj1.jpg', IMAGE_REGS)
    img2 = Image('mj2.jpg', IMAGE_REGS)

    print(img1.compare(img2))