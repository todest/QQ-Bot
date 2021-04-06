import asyncio
import os
import subprocess

from graia.application import MessageChain, Friend
from graia.application.message.elements.internal import Plain

from app.plugin.plugin import Plugin
from app.util.decorator import *
from app.util.tools import app_path


def pretreatment(src, ext):
    src = '\n'.join(src.split('\n')[1:]).replace('\r', '')
    with open(os.sep.join([app_path(), 'tmp', 'run.' + ext]), 'w', encoding='utf-8')as f:
        f.write(src)


def py3(source):
    pretreatment(source, 'py')
    with open(os.sep.join([app_path(), 'tmp', 'py.out']), 'w', encoding='utf-8')as f:
        subprocess.call('python3 run.py', timeout=5, shell=True, stdout=f, cwd=os.sep.join([app_path(), 'tmp']))
    with open(os.sep.join([app_path(), 'tmp', 'py.out']), 'r', encoding='utf-8')as f:
        ret = f.read()
    return ret


class Run(Plugin):
    entry = ['.run']
    brief_help = '\r\n[√]\t运行脚本：run'
    full_help = '运行各语言脚本'

    @permission_required(level='ADMIN')
    async def process(self):
        if not self.msg:
            self.print_help()
            return
        if self.msg[0] == 'py3':
            out = py3(self.message.asDisplay())
            self.resp = MessageChain.create([
                Plain(out)
            ])
        else:
            self.args_error()


if __name__ == '__main__':
    a = Run(MessageChain.create([Plain('.run')]), Friend.construct(id=1123))
    asyncio.run(a.get_resp())
    print(a.resp)
