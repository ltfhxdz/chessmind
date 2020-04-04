#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import socket
import json
import base64
import requests
from datetime import datetime


class chessnet:

    @staticmethod
    def getToken():
        appid = '18990061'
        client_id = '7L0MScc8VOgob1x51A69gmYr'
        client_secret = 'XuEOKrU6N0GE8PKGBdONnWSb7mKrwm74'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'
        host += "&client_id=%s&client_secret=%s" % (client_id, client_secret)
        session = requests.Session()
        response = session.get(host)
        access_token = response.json().get("access_token")
        # print(access_token)
        return access_token

    @staticmethod
    def uploadImage(imagePath, jsonPath):
        request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/chessx"
        with open(imagePath, 'rb') as f:
            image = base64.b64encode(f.read()).decode('UTF8')
        headers = {'Content-Type': 'application/json'}
        params = {"image": image}
        params = json.dumps(params)
        request_url = request_url + "?access_token=" + chessnet.getToken()
        session = requests.Session()
        response = session.post(request_url, headers=headers, data=params)
        content = response.content.decode('UTF-8')
        resultDict = json.loads(content)
        print(resultDict['results'])
        with open(jsonPath, 'w') as file_obj:
            json.dump(resultDict, file_obj)


# print(datetime.now())
# print(sys.version)
#
# domain = "aip.baidubce.com"
# myaddr = socket.getaddrinfo(domain, 'https')
# print(str(domain) + " = " + myaddr[0][4][0])
#
# start = time.time()
#
# # chessnet.uploadImage()
#
#
# end = time.time()
# print('Running time: %1.2f Seconds' % (end - start))
