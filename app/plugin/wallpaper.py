from app.plugin.base import Plugin
from graia.application import MessageChain, Image


class Test(Plugin):
	cmd = '.wp'
	brief_help = cmd + '\t动漫图片\r\n'
	full_help = '动漫图片来源于新浪'

	def process(self):
		try:
			self.resp = MessageChain.create([
				Image.fromNetworkAddress(r'http://api.btstu.cn/sjbz/?lx=dongman')
			])
		except Exception as e:
			print(e)
			self.unkown_error()
