import time
import random
from app.resource.love import *
from app.plugin.base import Plugin
from graia.application import Member, MessageChain

from graia.application.message.elements.internal import At, Plain, Image


class Cp(Plugin):
	entry = ['.cp']
	brief_help = entry[0] + '\t群内每天随机组CP\r\n'
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
				if inx & 1:
					cp = inx - 1
				else:
					cp = inx + 1
				break
		random.seed()
		self.resp = MessageChain.create([
			At(self.member.id),
			Plain(' 你今日配对的CP是：'),
			Image.fromNetworkAddress('https://q1.qlogo.cn/g?b=qq&nk=' + str(members[cp]['id']) + '&s=640'),
			Plain('昵称：%s\r\n\r\n' % members[cp]['name']),
			Plain(random.choice(cp_say))
		])
