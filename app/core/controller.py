from app.plugin import *
from app.core.settings import *
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain


class Controller:
	def __init__(self, *args):
		"""存储消息"""
		for arg in args:
			if isinstance(arg, MessageChain):
				self.message = arg  # 消息内容
			elif isinstance(arg, Friend) or isinstance(arg, Group):
				self.source = arg  # 消息来源 好友/群聊
			elif isinstance(arg, Member):
				self.member = arg  # 群聊消息发送者
			elif isinstance(arg, GraiaMiraiApplication):
				self.app = arg  # 程序执行主体

	async def process_event(self):
		"""处理消息"""
		msg = self.message.asDisplay()
		send_help = False  # 是否为主菜单帮助
		resp = '.help\t显示帮助指令\r\n'

		# 判断是否在权限允许列表
		if isinstance(self.source, Friend):
			if self.source.id not in ACTIVE_USER:
				return
		elif isinstance(self.source, Group):
			if self.source.id not in ACTIVE_GROUP:
				return
		if msg[0] not in '.,;。，；/\\':  # 判断是否为指令
			return

		# 指令规范化
		if not msg[0] == '.':
			msg = '.' + msg[1:]

		# 判断是否为主菜单帮助
		if msg.startswith('.help'):
			send_help = True

		# 加载插件
		for plugin in base.Plugin.__subclasses__():
			obj = None
			if isinstance(self.source, Friend):
				obj = plugin(msg, self.source)
			elif isinstance(self.source, Group):
				obj = plugin(msg, self.member)
			if send_help:  # 主菜单帮助获取
				resp += obj.brief_help
			elif msg.startswith(obj.entry):  # 指令执行
				resp = obj.get_resp()
				if resp:
					await self._do_send(resp)
				break

		# 主菜单帮助发送
		if send_help:
			await self._do_send(MessageChain.create([Plain(resp)]))

	async def _do_send(self, resp):
		"""发送消息"""
		if isinstance(self.source, Friend):  # 发送好友消息
			await self.app.sendFriendMessage(self.source, resp)
		elif isinstance(self.source, Group):  # 发送群聊消息
			await self.app.sendGroupMessage(self.source, resp)
