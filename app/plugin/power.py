import os
import subprocess

from graia.application import MessageChain
from graia.application.message.elements.internal import At, Plain

from app.core.settings import *
from app.plugin.base import Plugin
from app.util.tools import isstartswith


class Admin(Plugin):
    entry = ['.power', '.电源', '.p']
    brief_help = '\r\n[√]\t电源：p'
    full_help = \
        '.电源/.p\t仅限管理员使用！\r\n' \
        '.电源/.p k\t关闭机器人\r\n' \
        '.电源/.p r\t重启机器人\r\n' \
        '.电源/.p u [timeout]\t升级机器人(默认超时时间为10秒)\r\n'
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
                    shell += f' -g {self.group.id} -t {self.member.id}'
                elif hasattr(self, 'friend'):
                    shell += f' -t {self.friend.id}'
                if isstartswith(self.msg[0], 'k'):
                    os.system(shell + ' -k')
                elif isstartswith(self.msg[0], 'u'):
                    timeout = 10
                    if len(self.msg) == 2 and self.msg[1].isdigit():
                        timeout = int(self.msg[1])
                    p = subprocess.Popen(shell + ' -u', shell=True)
                    try:
                        p.wait(timeout)
                    except subprocess.TimeoutExpired:
                        p.kill()
                        if hasattr(self, 'group'):
                            self.resp = MessageChain.create([
                                At(self.member.id),
                                Plain(" 升级超时！")
                            ])
                        else:
                            self.resp = MessageChain.create([
                                Plain("升级超时！")
                            ])
                elif isstartswith(self.msg[0], 'r'):
                    os.system(shell + ' -r')
            else:
                self.args_error()
                return
        except Exception as e:
            print(e)
            self.unkown_error()
