import asyncio
import hashlib
import random
import string
import time
from urllib.parse import urlencode

import requests
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from app.core.config import *
from app.plugin.base import Plugin


def nonce_str():
    length = random.randint(1, 33)
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, length))
    return rand_str


def ai_bot(question):
    params = {
        'app_id': APP_ID,
        'session': LOGIN_QQ,
        'time_stamp': int(time.time()),
        'nonce_str': nonce_str(),
        'question': question
    }
    encode_url = urlencode(sorted(params.items(), key=lambda k: k[0]))
    encode_url += f'&app_key={APP_KEY}'
    sign = hashlib.md5(encode_url.encode('utf-8')).hexdigest().upper()
    params.update({'sign': sign})
    url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    response = requests.post(url, data=params)
    return response.json()['data']['answer']


class Chat(Plugin):
    entry = [' ']
    brief_help = '闲聊'
    full_help = '闲聊'

    async def process(self):
        msg = ''.join(i.dict()['text'] for i in self.message.get(Plain))[2:].strip()
        answer = '你说啥？' if not msg else ai_bot(msg).strip()
        self.resp = MessageChain.create([
            Plain(answer if answer else '我好像忘了什么...')
        ])


if __name__ == '__main__':
    a = Chat(MessageChain.create([Plain('. 123')]))
    asyncio.run(a.get_resp())
    print(a.resp)
