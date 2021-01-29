from app.util.parse import *
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain


class Plugin:
	"""子类必须重写这三个属性

	@:param entry: 程序入口点参数

	@:param brief_help: 简短帮助，显示在主帮助菜单

	@:param full_help: 完整帮助，显示在插件帮助菜单
	"""
	entry = '.plugin'
	brief_help = entry + 'this is a brief help.'
	full_help = 'this is a detail help.'

	def __init__(self, msg, source=None):
		"""根据需求可重写此构造方法"""
		self.msg: List[str] = parse_args(msg.asDisplay())
		self.message: MessageChain = msg
		self.source = source
		self.resp = None

	def _pre_check(self):
		"""此方法检查是否为插件帮助指令"""
		if self.msg:
			if self.msg[0] == 'help':
				self.resp = MessageChain.create([Plain(
					self.full_help
				)])

	def unkown_error(self):
		"""未知错误默认回复消息"""
		self.resp = MessageChain.create([Plain(
			'未知错误，请联系管理员处理！'
		)])

	def args_error(self):
		"""参数错误默认回复消息"""
		self.resp = MessageChain.create([Plain(
			'输入的参数错误！'
		)])

	def index_error(self):
		"""索引错误默认回复消息"""
		self.resp = MessageChain.create([Plain(
			'索引超出范围！'
		)])

	def arg_type_error(self):
		"""类型错误默认回复消息"""
		self.resp = MessageChain.create([Plain(
			'参数类型错误！'
		)])

	def point_not_enough(self):
		self.resp = MessageChain.create([Plain(
			'你的积分不足哦！'
		)])

	def process(self):
		"""子类必须重写此方法，此方法用于修改要发送的信息内容"""
		raise NotImplementedError

	def get_resp(self):
		"""程序默认调用的方法以获取要发送的信息"""
		self._pre_check()
		if not self.resp:
			self.process()
		if self.resp:
			return self.resp
		else:
			return None
