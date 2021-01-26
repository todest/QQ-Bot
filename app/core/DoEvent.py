from .settings import *
from ..plugin.Jrrp import *
from ..plugin.BotUtil import *
from ..plugin.hitokoto import *
from ..plugin.McServerStatus import *
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At


class DoEvent:
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
		if isinstance(self.source, Friend):
			if self.source.id not in ACTIVE_USER:
				return
		elif isinstance(self.source, Group):
			if self.source.id not in ACTIVE_GROUP:
				return
		else:
			return
		msg = self.message.asDisplay()
		if msg.startswith('.help'):
			await self.__do_help()
		elif msg.startswith('.jrrp'):
			await self.__do_jrrp()
		elif msg.startswith('.mcinfo'):
			await self.__do_mcinfo(msg)
		elif msg.startswith('.say'):
			await self._do_say(msg)

	async def __do_send(self, resp):
		if isinstance(self.source, Friend):
			await self.app.sendFriendMessage(self.source, MessageChain(__root__=resp))
		elif isinstance(self.source, Group):
			await self.app.sendGroupMessage(self.source, MessageChain(__root__=resp))

	async def __do_error(self):
		resp = [Plain('未知错误，请联系管理员！')]
		await self.__do_send(resp)

	async def __do_help(self):
		resp = [Plain(
			".help\t显示帮助指令\r\n"
			".jrrp\t今日人品\r\n"
			".say [type]/[help]\t一言\r\n"
			".mcinfo [host] [port] [timeout]\t显示MC服务器状态"
		)]
		await self.__do_send(resp)

	async def __do_jrrp(self):
		if isinstance(self.source, Friend):
			resp = [Plain(Jrrp(self.source.id).print_jrrp())]
			await self.app.sendFriendMessage(self.source, MessageChain(__root__=resp))
		elif isinstance(self.source, Group):
			message = Jrrp(self.member.id).print_jrrp()
			resp = [At(self.member.id, display=self.member.name), Plain(' '), Plain(message)]
			await self.app.sendGroupMessage(self.source, MessageChain(__root__=resp))

	async def __do_mcinfo(self, msg):
		msg = parseArgs(msg)
		try:
			resp = [Plain(StatusPing(*msg).get_status(str_format=True))]
			await self.__do_send(resp)
		except EnvironmentError as e:
			print(e)
			await self.__do_send([Plain('由于目标计算机积极拒绝，无法连接。服务器可能已关闭。')])
		except Exception as e:
			print(e)
			await self.__do_error()

	async def _do_say(self, msg):
		msg = parseArgs(msg)
		if msg:
			msg = msg[0]
			if msg == 'help':
				await self.__do_send([Plain(getHitokotoHelp())])
				return
		try:
			resp = [Plain(getHitokoto(msg))]
			await self.__do_send(resp)
		except AssertionError as e:
			print(e)
			await self.__do_send([Plain('输入参数错误！')])
		except Exception as e:
			print(e)
			await self.__do_error()
