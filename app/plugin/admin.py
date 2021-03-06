import asyncio

from app.core.settings import *
from app.plugin.base import Plugin
from app.util.tools import isstartswith
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain


class Admin(Plugin):
    entry = ['.sys', '.系统']
    brief_help = '\r\n[√]\t系统：sys'
    full_help = \
        '.管理\t.sys\t仅限管理员使用！\r\n' \
        '.管理\t.sys au [qq]\t临时添加用户\r\n' \
        '.管理\t.sys du [qq]\t临时移除用户\r\n' \
        '.管理\t.sys ag [qg]\t临时添加群组\r\n' \
        '.管理\t.sys dg [qg]\t临时移除群组'
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
