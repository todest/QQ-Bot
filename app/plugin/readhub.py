import asyncio
import json
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain, Image as Img

from app.plugin.base import Plugin
from app.util.tools import line_break


class ReadHub(Plugin):
    entry = ['.news', '.新闻']
    brief_help = '\r\n[√]\t新闻：news'
    full_help = '.新闻/.news [num]\r\n获取num数量的科技新闻信息，默认数量为5。'

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
            return "HTTP GET ERROR!"
        news_digest = ""
        resp_json = json.loads(req.text)
        news_list = resp_json["data"]
        for news in news_list:
            news_digest += news["title"] + "\n"
        return news_digest

    async def process(self):
        try:
            char_counts = 40
            font_size = 30
            padding = 60
            news = self._get_news().split('\n')[:-1]
            for i in range(len(news)):
                news[i] = f'{i + 1}. {news[i]}。'

            title = '一觉醒来世界发生了什么？'
            news = line_break('\n\n'.join(news) + '\n', char_counts=char_counts)

            im = Image.new("L", (char_counts * font_size // 2 + padding * 2,
                                 font_size * news.count('\n') + padding * 3), "WHITE")
            dr = ImageDraw.Draw(im)

            h1 = ImageFont.truetype(font='msyhbd.ttc', size=int(font_size * 1.2))
            font = ImageFont.truetype(font='simsun.ttc', size=font_size)

            dr.text((padding, padding), text=title, font=h1, fill='BLACK', spacing=4)
            dr.text((padding, padding * 2), text=news, font=font, fill='BLACK', spacing=4)
            im_bytes = BytesIO()
            im.save(im_bytes)
            self.resp = MessageChain.create([
                Img.fromUnsafeBytes(im_bytes.getvalue())
            ])
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
    a = ReadHub(MessageChain.create([Plain('.news 20')]))
    asyncio.run(a.get_resp())
    print(a.resp)
