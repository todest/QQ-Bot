from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from app.core.config import DEBUG, change_debug
from app.trigger.trigger import Trigger
from app.util.decorator import permission_required


class ChangeMode(Trigger):
    async def process(self):
        if self.msg[0] == '.mode':
            await self.change_mode()

    @permission_required(level='ADMIN')
    async def change_mode(self):
        if DEBUG:
            await self.do_send(MessageChain.create([
                Plain('已退出DEBUG模式！')
            ]))
        else:
            await self.do_send(MessageChain.create([
                Plain('已进入DEBUG模式！')
            ]))
        change_debug()
        self.as_last = True
