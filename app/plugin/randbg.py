import asyncio
import os
import platform

from graia.application import MessageChain, Image
from graia.application.message.elements.internal import Plain

from app.plugin.base import Plugin
from app.util.tools import app_path


class RandBg(Plugin):
    entry = ['.setu', '.st', '.色图']
    brief_help = '\r\n[√]\t色图：setu'
    full_help = '.setu [seed] seed为正整数，默认为随机数\r\n' \
                '生成随机色图'

    async def process(self):
        try:
            if platform.system().lower() == 'linux':
                shell = os.sep.join([app_path(), 'exec'])
                if self.msg:
                    shell += ' ' + self.msg[0]
                os.system('ulimit -s 102400')
                os.system(f'cd {shell} && ./randbg')
                os.system(f'optipng {app_path()}/tmp/rgb.png')
            else:
                shell = os.sep.join([app_path(), 'exec', 'randbg.exe'])
                if self.msg:
                    shell += ' ' + self.msg[0]
                os.system(f'cd {app_path()}\\exec && {shell}')
            self.resp = MessageChain.create([
                Image.fromLocalFile(os.sep.join([app_path(), 'tmp', 'rgb.png']))
            ])
        except Exception as e:
            print(e)
            self.unkown_error()


if __name__ == '__main__':
    a = RandBg(MessageChain.create([Plain('.setu 123')]))
    asyncio.run(a.get_resp())
    print(a.resp)
