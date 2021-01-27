from app.util.parse import *
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain


class Plugin:
	cmd = '.plugin'
	brief_help = 'this is a brief help.'
	full_help = 'this is a detail help.'

	def __init__(self, msg, source=None):
		self.msg = parse_args(msg)
		self.source = source
		self.resp = None

	def _pre_check(self):
		if self.msg:
			if self.msg[0] == 'help':
				self.resp = MessageChain.create([Plain(
					self.full_help
				)])

	def unkown_error(self):
		self.resp = MessageChain.create([Plain(
			'未知错误，请联系管理员处理！'
		)])

	def args_error(self):
		self.resp = MessageChain.create([Plain(
			'输入的参数错误！'
		)])

	def index_error(self):
		self.resp = MessageChain.create([Plain(
			'索引超出范围！'
		)])

	def arg_type_error(self):
		self.resp = MessageChain.create([Plain(
			'参数类型错误！'
		)])

	def process(self):
		raise NotImplementedError

	def get_resp(self):
		self._pre_check()
		if not self.resp:
			self.process()
		if self.resp:
			return self.resp
