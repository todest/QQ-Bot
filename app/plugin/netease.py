import asyncio

import requests
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from app.plugin.plugin import Plugin


class NetEase(Plugin):
    entry = ['.wyy', '.网易云']
    brief_help = '\r\n[√]\t网易云热评：wyy'
    full_help = '网易云热评，加上任意参数为网抑云热评！'

    async def process(self):
        if self.msg:
            req = requests.get('https://api.lo-li.icu/wyy/')
            self.resp = MessageChain.create([
                Plain(req.text)
            ])
        else:
            req = requests.get('https://api.66mz8.com/api/music.163.php?format=json')
            ans = req.json()
            self.resp = MessageChain.create([
                Plain('歌曲：%s\r\n' % ans['name']),
                Plain('昵称：%s\r\n' % ans['nickname']),
                Plain('评论：%s' % ans['comments'])
            ])


if __name__ == '__main__':
    a = NetEase(MessageChain.create([Plain('.wyy 1')]))
    asyncio.run(a.get_resp())
    print(a.resp)
