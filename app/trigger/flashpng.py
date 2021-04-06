from graia.application import MessageChain
from graia.application.message.elements.internal import FlashImage, Plain, Image

from app.trigger.trigger import Trigger


class FlashPng(Trigger):
    async def process(self):
        flash = self.message[FlashImage]
        if not flash:
            return
        await self.do_send(MessageChain.create([
            Plain('识别到闪照如下：\r\n'),
            Image.fromNetworkAddress(flash[0].dict()['url'])
        ]))
        self.as_last = True
