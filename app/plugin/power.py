import os

from app.core.settings import *
from app.plugin.base import Plugin
from app.util.tools import isstartswith
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain


class Admin(Plugin):
    entry = ['.power', '.电源']
    brief_help = '\r\n[√]\t电源：p'
    full_help = \
        '.管理\t.p\t仅限管理员使用！\r\n' \
        '.管理\t.p k\t关闭机器人\r\n' \
        '.管理\t.p r\t重启机器人\r\n' \
        '.管理\t.p u\t升级机器人\r\n' \
        '.管理\t.p run\t执行python代码'
    hidden = True

    async def process(self):
        if not self.check_admin():
            self.not_admin()
        if not self.msg:
            self.print_help()
            return
        try:
            if isstartswith(self.msg[0], ['k', 'u', 'r']):
                shell = HOME_PATH + f'run.sh'
                if hasattr(self, 'group'):
                    shell += f' -g {self.group.id} -e {self.member.id}'
                elif hasattr(self, 'friend'):
                    shell += f' -e {self.friend.id}'
                if isstartswith(self.msg[0], 'k'):
                    os.system(shell + ' -k')
                elif isstartswith(self.msg[0], 'u'):
                    os.system(shell + ' -u')
                elif isstartswith(self.msg[0], 'r'):
                    os.system(shell)
            elif isstartswith(self.msg[0], 'run'):
                msg = self.message.asDisplay().strip().split('\r\n').pop(0)
                self.resp = MessageChain.create([])
                for item in msg:
                    ret = eval(item)
                    if ret:
                        self.resp.plus(MessageChain.create([
                            Plain(str(ret))
                        ]))
            else:
                self.args_error()
                return
        except Exception as e:
            print(e)
            self.unkown_error()
