import asyncio
import hashlib
import random
import string
import time
from urllib.parse import urlencode

import requests
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain
from retrying import retry

from app.core.config import *
from app.plugin.plugin import Plugin


def nonce_str():
    length = random.randint(1, 33)
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, length))
    return rand_str


no_answer = [
    '我好像忘了什么...',
    '你刚刚说什么？',
    '啊？',
    '我忘了你说的啥...',
    '我好像失忆了...',
    '等等，我想下要说什么!',
    '没理解你什么意思',
    '我听不懂你在说什么',
    '不听不听，王八念经！',
    '我有权保持沉默！',
    'No Answer!'
    'Pardon？',
    'Sorry, can you say that again?',
    'Could you repeat that please?',
    'Come again?',
    'I didn’t catch your meaning.',
    'I don’t get it.',
    'I didn’t follow you.',
    'I can’t hear you.',
    'Could you speak up a little bit?',
    'Could you slow down a little bit?'
]


@retry(stop_max_attempt_number=5, wait_fixed=1000)
def ai_bot(question):
    config = Config()
    params = {
        'app_id': config.APP_ID,
        'session': config.LOGIN_QQ,
        'time_stamp': int(time.time()),
        'nonce_str': nonce_str(),
        'question': question
    }
    encode_url = urlencode(sorted(params.items(), key=lambda k: k[0]))
    encode_url += f'&app_key={config.APP_KEY}'
    sign = hashlib.md5(encode_url.encode('utf-8')).hexdigest().upper()
    params.update({'sign': sign})
    url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    response = str(requests.post(url, data=params).json()['data']['answer']).strip()
    if not response:
        raise Exception
    return response


class Chat(Plugin):
    entry = ['. ']
    brief_help = '\r\n[√]\t闲聊：[空格]'
    full_help = '闲聊'

    async def process(self):
        msg = ''.join(i.dict()['text'] for i in self.message.get(Plain))[2:].strip()
        try:
            answer = ai_bot(msg)
        except Exception:
            answer = random.choice(no_answer)
        self.resp = MessageChain.create([
            Plain(answer)
        ])
        # if random.randint(0, 10):
        #     self.resp = MessageChain.create([
        #         Plain(answer)
        #     ])
        # else:
        #     self.resp = MessageChain.create([
        #         Voice.fromLocalFile(os.sep.join([app_path(), 'tmp', 'rgb.png']))
        #     ])


if __name__ == '__main__':
    a = Chat(MessageChain.create([Plain('. 123')]))
    asyncio.run(a.get_resp())
    print(a.resp)
