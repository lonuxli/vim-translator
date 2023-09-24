# coding=utf-8
from __future__ import unicode_literals

import base64
import hashlib
import json
import random
import time
import uuid
from sys import argv, stdout
from urllib import error, parse, request
import requests

Url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
youdao_url = 'https://openapi.youdao.com/api'
app_id = "227be68bc7a4d872"
app_key = "Jasy36fJdtME8WvExlPFkI6fYnvaQ03w"


def get_result(query):
    query = base64.b64decode(query).decode('utf-8')
    return _get_result(query)


def _get_result(query):

    if(len(query) <= 20):
        input_text = query
    elif(len(query) > 20):
        input_text = query[:10] + str(len(query)) + query[-10:]

    time_curtime = int(time.time())
    uu_id = uuid.uuid4()

    sign = hashlib.sha256((app_id + input_text + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()

    data = {
        'q':query,   # 翻译文本
        'from':"AUTO",   # 源语言
        'to':"AUTO",   # 翻译语言
        'appKey':app_id,   # 应用id
        'salt':uu_id,   # 随机生产的uuid码
        'sign':sign,   # 签名
        'signType':"v3",   # 签名类型，固定值
        'curtime':time_curtime,   # 秒级时间戳
        'domain':"computers"
    }

    result = requests.get(youdao_url, params = data)   # 获取返回的json()内容

    res = result.json()
    if res['errorCode'] != 0:
        if res['errorCode'] == 40:
            return 'Err:无结果'
        if res['errorCode'] == 50:
            return 'Err:签名错误'
    return query + '\n' + "翻译结果:" + res["translation"][0]

if __name__ == '__main__':
    if len(argv) >= 2:
        stdout.write(str(get_result(argv[1])))
    stdout.flush()
