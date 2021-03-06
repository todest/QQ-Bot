import asyncio
import os

from app.core.settings import *
from app.plugin.base import Plugin
from app.util.tools import isstartswith
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain


class Admin(Plugin):
    entry = ['.sys', '.系统']
    brief_help = '\r\n[√]\t系统：sys'
    full_help = \
        '.管理/.sys\t仅限管理员使用！\r\n' \
        '.管理/.sys k\t关闭机器人\r\n' \
        '.管理/.sys r\t重启机器人\r\n' \
        '.管理/.sys u\t升级机器人\r\n' \
        '.管理/.sys run\t执行python代码\r\n' \
        '.管理/.sys au [qq]\t临时添加用户\r\n' \
        '.管理/.sys du [qq]\t临时移除用户\r\n' \
        '.管理/.sys ag [qg]\t临时添加群组\r\n' \
        '.管理/.sys dg [qg]\t临时移除群组'
    hidden = True

    async def process(self):
        if not self.check_admin():
            self.not_admin()
        if not self.msg:
            self.print_help()
            return
        try:
            if len(self.msg) != 2:
                self.args_error()
                return
            assert self.msg[1].isdigit()
            if isstartswith(self.msg[0], 'au'):
                ACTIVE_USER.append(int(self.msg[1]))
            elif isstartswith(self.msg[0], 'du'):
                if int(self.msg[1]) not in ACTIVE_USER:
                    self.resp = MessageChain.create([Plain(
                        '未找到该用户！'
                    )])
                    return
                ACTIVE_USER.remove(int(self.msg[1]))
            elif isstartswith(self.msg[0], 'ag'):
                ACTIVE_GROUP.append(int(self.msg[1]))
            elif isstartswith(self.msg[0], 'dg'):
                if int(self.msg[1]) not in ACTIVE_GROUP:
                    self.resp = MessageChain.create([Plain(
                        '未找到该群组！'
                    )])
                    return
                ACTIVE_GROUP.remove(int(self.msg[1]))
            elif isstartswith(self.msg[0], ['k', 'u', 'r']):
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
            self.exec_success()
        except AssertionError as e:
            print(e)
            self.args_error()
        except Exception as e:
            print(e)
            self.unkown_error()


if __name__ == '__main__':
    a = Admin(MessageChain.create([Plain(
        '.admin au 123'
    )]))
    asyncio.run(a.get_resp())
    print(a.resp)
