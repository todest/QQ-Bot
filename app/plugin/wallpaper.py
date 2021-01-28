from app.plugin.base import Plugin
from graia.application import MessageChain, Image


class Test(Plugin):
	cmd = '.wp'
	brief_help = cmd + '\t必应壁纸\r\n'
	full_help = '壁纸来源于必应。'

	def process(self):
		try:
			self.resp = MessageChain.create([
				Image.fromNetworkAddress(r'https://bing.ioliu.cn/v1/rand?w=1920&h=1080')
			])
		except Exception as e:
			print(e)
			self.unkown_error()
