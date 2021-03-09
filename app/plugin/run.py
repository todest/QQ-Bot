import asyncio

from graia.application import MessageChain, Friend
from graia.application.message.elements.internal import Plain

from app.plugin.base import Plugin
from app.util.decorator import *


class Run(Plugin):
    entry = ['.run']
    brief_help = '\r\n[√]\t运行脚本：run'
    full_help = '运行python3脚本'

    @permission_required(level='ADMIN')
    async def process(self):
        if not self.msg:
            self.print_help()
            return


if __name__ == '__main__':
    a = Run(MessageChain.create([Plain('.run')]), Friend.construct(id=1123792492))
    asyncio.run(a.get_resp())
    print(a.resp)
