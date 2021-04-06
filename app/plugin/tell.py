from app.plugin.plugin import Plugin
from graia.application import MessageChain

from graia.application.message.elements.internal import Plain, At

from app.util.decorator import permission_required


class Tell(Plugin):
    entry = ['.tell']
    brief_help = '\r\n[√]\t发信：tell'
    full_help = '管理员控制机器人向某个群发送消息。\r\n' \
                '.tell [群号] [内容]'
    hidden = True

    @permission_required(level='ADMIN')
    async def process(self):
        if not self.msg or len(self.msg) < 2:
            return
        assert self.msg[0].isdigit()
        if not await self.app.getGroup(int(self.msg[0])):
            self.resp = MessageChain.create([Plain(
                '没有找到此群聊！'
            )])
            return
        self.resp = MessageChain.create([])
        for item in self.msg[1:]:
            if item[0] == '@' and await self.app.getMember(int(self.msg[0]), int(item[1:])):
                self.resp.plus(MessageChain.create([
                    At(int(item[1:])),
                    Plain(' ')
                ]))
            else:
                self.resp.plus(MessageChain.create([
                    Plain(item)
                ]))
        await self.app.sendGroupMessage(int(self.msg[0]), self.resp)
        self.resp = None
