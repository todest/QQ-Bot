import json
import requests

from app.plugin.base import Plugin
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain


class ReadHub(Plugin):
	entry = '.news'
	brief_help = entry + ' [num](1~20)\t科技新闻\r\n'
	full_help = '获取指定数量的科技新闻信息，默认数量为5。'

	def _get_news(self) -> str:
		if self.msg:
			self.msg = self.msg[0]
		else:
			self.msg = '5'
		self.msg = int(self.msg)
		assert self.msg in range(1, 21)
		api = "https://api.readhub.cn/topic?lastCursor=&pageSize=" + str(self.msg)
		req = requests.get(url=api)
		if req.status_code != 200:
			return "".join("HTTP GET ERROR!")
		news_digest = ""
		resp_json = json.loads(req.text)
		news_list = resp_json["data"]
		for index, news in enumerate(news_list):
			if index == 0:
				news_digest += news["title"]
			else:
				news_digest += "\r\n\r\n" + news["title"]
		return news_digest

	def process(self):
		try:
			self.resp = MessageChain.create([Plain(
				self._get_news()
			)])
		except ValueError as e:
			print(e)
			self.arg_type_error()
		except AssertionError as e:
			print(e)
			self.index_error()
		except Exception as e:
			print(e)
			self.unkown_error()


if __name__ == '__main__':
	a = ReadHub('.news')
	print(a.get_resp())
