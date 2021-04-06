import asyncio

from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from app.core.settings import *
from app.entities.group import BotGroup
from app.entities.user import BotUser
from app.plugin.plugin import Plugin
from app.util.decorator import permission_required
from app.util.tools import isstartswith


class Admin(Plugin):
    entry = ['.sys', '.系统']
    brief_help = '\r\n[√]\t系统：sys'
    full_help = \
        '.管理/.sys\t仅限管理员使用！\r\n' \
        '.管理/.sys au [qq]\t添加用户\r\n' \
        '.管理/.sys du [qq]\t移除用户\r\n' \
        '.管理/.sys ag [qg]\t添加群组\r\n' \
        '.管理/.sys dg [qg]\t移除群组'
    hidden = True

    @permission_required(level='ADMIN')
    async def process(self):
        if not self.msg:
            self.print_help()
            return
        try:
            if isstartswith(self.msg[0], 'au'):
                assert len(self.msg) == 2 and self.msg[1].isdigit()
                BotUser(int(self.msg[1]), active=1)
                self.resp = MessageChain.create([
                    Plain('添加成功！')
                ])
            elif isstartswith(self.msg[0], 'du'):
                assert len(self.msg) == 2 and self.msg[1].isdigit()
                if int(self.msg[1]) not in ACTIVE_USER:
                    self.resp = MessageChain.create([Plain(
                        '未找到该用户！'
                    )])
                    return
                with MysqlDao() as db:
                    res = db.update('UPDATE user SET active=0 where qq=%s', [int(self.msg[1])])
                if res:
                    self.resp = MessageChain.create([
                        Plain('取消成功！')
                    ])
            elif isstartswith(self.msg[0], 'ag'):
                assert len(self.msg) == 2 and self.msg[1].isdigit()
                BotGroup(int(self.msg[1]), active=1)
                self.resp = MessageChain.create([
                    Plain('添加成功！')
                ])
            elif isstartswith(self.msg[0], 'dg'):
                assert len(self.msg) == 2 and self.msg[1].isdigit()
                if int(self.msg[1]) not in ACTIVE_GROUP:
                    self.resp = MessageChain.create([Plain(
                        '未找到该群组！'
                    )])
                    return
                with MysqlDao() as db:
                    res = db.update('UPDATE `group` SET active=0 WHERE group_id=%s', [int(self.msg[1])])
                if res:
                    self.resp = MessageChain.create([
                        Plain('取消成功！')
                    ])
            elif isstartswith(self.msg[0], 'ul'):
                with MysqlDao() as db:
                    res = db.query(
                        "SELECT qq FROM user WHERE active=1"
                    )
                self.resp = MessageChain.create([Plain(
                    ''.join([f'{qq}\r\n' for (qq,) in res])
                )])
            elif isstartswith(self.msg[0], 'gl'):
                with MysqlDao() as db:
                    res = db.query(
                        "SELECT group_id FROM `group` WHERE active=1"
                    )
                self.resp = MessageChain.create([Plain(
                    ''.join([f'{group_id}\r\n' for (group_id,) in res])
                )])
            else:
                self.args_error()
                return
        except AssertionError as e:
            print(e)
            self.args_error()
        except Exception as e:
            print(e)
            self.unkown_error()


if __name__ == '__main__':
    a = Admin(MessageChain.create([Plain(
        '.sys au 123'
    )]))
    asyncio.run(a.get_resp())
    print(a.resp)
