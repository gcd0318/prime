from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import sys
sys.path.append(os.path.abspath('..'))

from base.utils import base64img, access_token
from base.utils import get_json, post_json

from aip import AipFace

class Face(object):

    def __init__(self, filename, regs, face_type='LIVE', quality_control='LOW'):
        app_id, api_key, secret_key = regs
        self.filename, self.face_type, self.quality_control = filename, face_type, quality_control
        self.base64 = base64img(filename)
        self.client = AipFace(app_id, api_key, secret_key)

    def __dict__(self):
        return {"image": self.base64.decode('utf-8'), "image_type": "BASE64", "face_type": self.face_type, "quality_control": self.quality_control}

    '''
    def _compare(self, aface):
        res = -1
        params = json.dumps(
            [
                self.__dict__(),
                aface.__dict__()
            ]
        )
        token = access_token(url='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.api_key + '&client_secret=' + self.secret_key,
            key='access_token')
        url = "https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=" + token
        headers = {'Content-Type': 'application/json'}
        data = json.loads(post_json(url, data=params, headers=headers))
        if data is not None:
            error_code = data.get('error_code')
            error_msg = data.get('error_msg')
            result = data.get('result')
            if (0 == error_code) and ('SUCCESS' == error_msg):
                res = result.get('score')
        return res
    '''

    def compare(self, aface):
        data = self.client.match([self.__dict__(), aface.__dict__()])
        if data is not None:
            error_code = data.get('error_code')
            error_msg = data.get('error_msg')
            result = data.get('result')
            if (0 == error_code) and ('SUCCESS' == error_msg):
                res = result.get('score')
        return res


if '__main__' == __name__:
    from config import FACE_REGS
    f1 = Face('mj1.jpg', FACE_REGS)
    f2 = Face('mj2.jpg', FACE_REGS)

    print(f1.compare(f2))
