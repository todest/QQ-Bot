import asyncio
import os
import platform

from graia.application import MessageChain, Image
from graia.application.message.elements.internal import Plain

from app.core.settings import EXEC_PATH
from app.plugin.base import Plugin


class RandBg(Plugin):
    entry = ['.setu', '.st', '.色图']
    brief_help = '\r\n[√]\t色图：setu'
    full_help = '.setu [seed] seed为正整数，默认为随机数\r\n' \
                '生成随机色图'

    async def process(self):
        try:
            shell = os.sep.join([EXEC_PATH, 'randbg'])
            if self.msg:
                shell += ' ' + self.msg[0]
            if not os.system(shell):
                if platform.system().lower() == 'linux':
                    os.system('optipng rgb.png')
                self.resp = MessageChain.create([
                    Image.fromLocalFile('rgb.png')
                ])
        except Exception as e:
            print(e)
            self.unkown_error()


if __name__ == '__main__':
    a = RandBg(MessageChain.create([Plain('.setu 123')]))
    asyncio.run(a.get_resp())
    print(a.resp)
