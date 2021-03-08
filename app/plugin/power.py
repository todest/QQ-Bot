import os
import subprocess
import threading
from time import sleep

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
        '.电源/.p u\t升级机器人\r\n'
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
                    p = subprocess.Popen([shell, '-u'])
                    try:
                        p.wait(10)
                    except subprocess.TimeoutExpired:
                        p.kill()
                elif isstartswith(self.msg[0], 'r'):
                    os.system(shell + ' -r')
            else:
                self.args_error()
                return
        except Exception as e:
            print(e)
            self.unkown_error()
