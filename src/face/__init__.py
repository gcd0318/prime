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

    def __init__(self, regs, filename, image_type="BASE64", face_type='LIVE', quality_control='LOW'):
        app_id, api_key, secret_key = regs
        self.filename, self.image_type, self.face_type, self.quality_control = filename, image_type, face_type, quality_control
        if 'BASE64' == image_type:
            self.image = base64img(filename).decode('utf-8')
        elif 'URL' == image_type:
            self.image = filename
        else:
            self.image = None
        self.client = AipFace(app_id, api_key, secret_key)

    def __dict__(self):
        return {"image": self.image, "image_type": self.image_type, "face_type": self.face_type, "quality_control": self.quality_control}

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

    def detect(self, options=None):
        face_num, faces = None, None
        if options is None:
            options = {}
#            options = {"face_field": "age", "max_face_num": 2, "face_type": "LIVE", "liveness_control": "LOW"}
        r = self.client.detect(self.image, self.image_type, options)
        print(r)
        if r is not None:
            result = r.get('result')
            face_num, faces = result.get('face_num'), result.get('face_list')
        return face_num, faces

    def compare(self, aface):
        r = self.client.match([self.__dict__(), aface.__dict__()])
        if r is not None:
            result = r.get('result')
            if (0 == r.get('error_code')) and ('SUCCESS' == r.get('error_msg')):
                res = result.get('score')
        return res

    def register(self, options=None):
        if options is None:
            options = {'max_face_num': 10}
#            options = {"user_info": "user's info", "quality_control": "NORMAL", "liveness_control": "LOW", "action_type": "REPLACE"}
        self.client.addUser(self.image, self.imageType, groupId, userId, options)

if '__main__' == __name__:
    from config import FACE_REGS
    f1 = Face(filename='mj1.jpg', regs=FACE_REGS)
    f2 = Face(filename='mj2.jpg', regs=FACE_REGS)

#    print(f1.compare(f2))
    print(f1.detect())
