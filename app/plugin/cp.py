import time
import random
from app.resource.love import *
from app.plugin.plugin import Plugin
from graia.application import MessageChain

from graia.application.message.elements.internal import At, Plain, Image


class Cp(Plugin):
    entry = ['.cp']
    brief_help = '\r\n[√]\t组CP：cp'
    full_help = '每天在群内组CP'

    async def process(self):
        member_list = await self.app.memberList(self.group.id)
        members = [{'id': member.id, 'name': member.name} for member in member_list]
        if len(members) & 1:
            bot_id = self.app.connect_info.account
            bot_name = (await self.app.getFriend(bot_id)).nickname
            members.append({'id': bot_id, 'name': bot_name})
        random.seed(time.strftime("%Y%m%d", time.localtime()))
        random.shuffle(members)
        cp = None
        for inx, item in enumerate(members):
            if item['id'] == self.member.id:
                cp = inx - 1 if inx & 1 else inx + 1
                break
        random.seed()
        self.resp = MessageChain.create([
            At(self.member.id),
            Plain(' 你今日配对的CP是：'),
            Image.fromNetworkAddress('https://q1.qlogo.cn/g?b=qq&nk=' + str(members[cp]['id']) + '&s=1'),
            Plain('昵称：%s\r\n\r\n' % members[cp]['name']),
            Plain(random.choice(cp_say))
        ])
