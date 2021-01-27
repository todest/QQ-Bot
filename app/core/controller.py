from app.plugin import *
from app.core.settings import *
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain

from graia.application.message.elements.internal import Plain


class Controller:
	def __init__(self, *args):
		for arg in args:
			if isinstance(arg, MessageChain):
				self.message = arg
			elif isinstance(arg, Friend) or isinstance(arg, Group):
				self.source = arg
			elif isinstance(arg, Member):
				self.member = arg
			elif isinstance(arg, GraiaMiraiApplication):
				self.app = arg

	async def process_event(self):
		msg = self.message.asDisplay()
		send_help = False
		resp = '.help\t显示帮助指令\r\n'
		if isinstance(self.source, Friend):
			if self.source.id not in ACTIVE_USER:
				return
		elif isinstance(self.source, Group):
			if self.source.id not in ACTIVE_GROUP:
				return
		elif not msg.startswith('.'):
			return
		if msg.startswith('.help'):
			send_help = True
		for plugin in base.Plugin.__subclasses__():
			obj = None
			if isinstance(self.source, Friend):
				obj = plugin(msg)
			elif isinstance(self.source, Group):
				obj = plugin(msg, self.member.id)
			if send_help:
				resp += obj.brief_help
			elif msg.startswith(obj.cmd):
				resp = obj.get_resp()
				await self._do_send(resp)
				break
		if send_help:
			await self._do_send(MessageChain.create([Plain(resp)]))

	async def _do_send(self, resp):
		if isinstance(self.source, Friend):
			await self.app.sendFriendMessage(self.source, resp)
		elif isinstance(self.source, Group):
			await self.app.sendGroupMessage(self.source, resp)
