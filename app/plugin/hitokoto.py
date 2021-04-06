import asyncio
import requests
from app.plugin.plugin import Plugin
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain


class Hitokoto(Plugin):
    entry = ['.say', '一言']
    brief_help = '\r\n[√]\t一言：say'
    full_help = \
        ".一言/.say [type] type列表如下:\r\n" \
        "a\t动画\r\n" \
        "b\t漫画\r\n" \
        "c\t游戏\r\n" \
        "d\t文学\r\n" \
        "e\t原创\r\n" \
        "f\t来自网络\r\n" \
        "g\t其他\r\n" \
        "h\t影视\r\n" \
        "i\t诗词\r\n" \
        "j\t网易云\r\n" \
        "k\t哲学\r\n" \
        "l\t抖机灵"

    async def process(self):
        try:
            self.resp = MessageChain.create([Plain(
                self._get_hitokoto()
            )])
        except AssertionError as e:
            print(e)
            self.args_error()
        except Exception as e:
            print(e)
            self.unkown_error()

    def _get_hitokoto(self) -> str:
        api_url = 'https://v1.hitokoto.cn'
        data = {
            'encode': 'text',
            'charset': 'utf-8'
        }
        if self.msg:
            assert self.msg[0] in [chr(i) for i in range(ord('a'), ord('m'))]
            data.update({'c': self.msg[0]})
        result = requests.get(api_url, params=data)
        result = result.content.decode('utf-8')
        return result


if __name__ == '__main__':
    a = Hitokoto(MessageChain.create([Plain('.say c')]))
    asyncio.run(a.get_resp())
    print(a.resp)
