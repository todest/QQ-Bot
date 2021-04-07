from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from app.core.config import Config
from app.trigger.trigger import Trigger
from app.util.decorator import permission_required


class ChangeMode(Trigger):
    async def process(self):
        if self.msg[0] == '.mode':
            await self.change_mode()

    @permission_required(level='ADMIN')
    async def change_mode(self):
        config = Config()
        if config.DEBUG:
            await self.do_send(MessageChain.create([
                Plain('>> 已退出DEBUG模式！\t\n>> 服务端进入工作状态！\r\n'),
                Plain('>> 消息来自%s端!' % ('服务' if config.ONLINE else 'DEBUG'))
            ]))
        else:
            await self.do_send(MessageChain.create([
                Plain('>> 已进入DEBUG模式！\r\n>> 服务端进入休眠状态！\r\n'),
                Plain('>> 消息来自%s端!' % ('服务' if config.ONLINE else 'DEBUG'))
            ]))
        config.change_debug()
        self.as_last = True
