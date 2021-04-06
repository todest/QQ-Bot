import asyncio

import requests
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from app.plugin.plugin import Plugin


def _get_djt() -> str:
    api_url = 'https://api.cyfan.top/dujitang'
    req = requests.get(api_url).content.decode('utf-8')
    return req[16:-3]


class DuJiTang(Plugin):
    entry = ['.jt', '.djt', '.dujitang']
    brief_help = '\r\n[√]\t鸡汤：jt'
    full_help = '毒鸡汤！！！'

    async def process(self):
        try:
            self.resp = MessageChain.create([Plain(
                _get_djt()
            )])
        except AssertionError as e:
            print(e)
            self.args_error()
        except Exception as e:
            print(e)
            self.unkown_error()


if __name__ == '__main__':
    a = DuJiTang(MessageChain.create([Plain('.jt')]))
    asyncio.run(a.get_resp())
    print(a.resp)
