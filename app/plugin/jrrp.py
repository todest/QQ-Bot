import time
import math
import random
import asyncio
from app.plugin.base import Plugin
from graia.application import MessageChain, Friend
from graia.application.message.elements.internal import Plain, At


def f(x, mul, sigma):
    return 5000 * (1.0 / (math.sqrt(2 * math.pi) * sigma) * (math.e ** (-(x - mul) ** 2 / (2 * sigma * sigma))))


class Jrrp(Plugin):
    entry = ['.jrrp', '人品', '今日人品']
    brief_help = '\r\n[√]\t今日人品：jrrp'
    full_help = \
        '.人品/.今日人品/.jrrp\r\n' \
        '获取你今日的人品值，人品值为百分制哦！'

    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.date = time.strftime("%Y%m%d", time.localtime())

    def _get_jrrp(self) -> int:
        rplist = []
        for i in range(0, 101):
            for j in range(int(f(i, mul=60, sigma=40))):
                rplist.append(i)
        random.seed(str((getattr(self, 'friend', None) or getattr(self, 'member', None)).id) + self.date)
        result = rplist[random.randint(0, len(rplist) - 1)]
        return result

    def _print_jrrp(self) -> str:
        result = self._get_jrrp()
        if result == 0:
            result = "你今天的人品值是：0，不要给我差评啊。"
        elif 0 < result < 10:
            result = "你今天的人品值是：%d，嗯，没错，是百分制。" % result
        elif 10 <= result < 50:
            result = "你今天的人品值是：%d，哇呜。。。" % result
        elif result == 50:
            result = "你今天的人品值是：%d，五五开。。。" % result
        elif 50 < result < 60:
            result = "你今天的人品值是：%d，还，，还行吧。。。" % result
        elif 60 <= result < 70:
            result = "你今天的人品值是：%d，是不错的一天呢！" % result
        elif 70 <= result < 80:
            result = "你今天的人品值是：%d，一般般啦！" % result
        elif 80 <= result < 90:
            result = "你今天的人品值是：%d，很不错的一天呢！" % result
        elif 90 <= result < 100:
            result = "你今天的人品值是：%d，好评如潮！！！" % result
        elif result == 100:
            result = "你今天的人品值是：%d，100! 100!! 100!!!" % result
        return result

    async def process(self):
        if hasattr(self, 'group'):
            self.resp = MessageChain.create([
                At(self.member.id),
                Plain(' ' + self._print_jrrp())
            ])
        else:
            self.resp = MessageChain.create([
                Plain(self._print_jrrp())
            ])


if __name__ == '__main__':
    a = Jrrp(MessageChain.create([Plain('.jrrp')]), Friend.construct(id='123'))
    asyncio.run(a.get_resp())
    print(a.resp)
