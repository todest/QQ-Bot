from app.plugin.base import Plugin
from graia.application import MessageChain, Image


class WallPaper(Plugin):
	entry = ['.wp', '.壁纸']
	brief_help = entry[0] + '\t必应壁纸\r\n'
	full_help = \
		'.壁纸/.wp\r\n' \
		'随机从必应获取分辨率为1920x1080的壁纸。'

	async def process(self):
		try:
			self.resp = MessageChain.create([
				Image.fromNetworkAddress(r'https://bing.ioliu.cn/v1/rand?w=1920&h=1080')
			])
		except Exception as e:
			print(e)
			self.unkown_error()
