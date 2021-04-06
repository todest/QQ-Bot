from typing import List

from graia.application import MessageChain, Friend, Group, Member, GraiaMiraiApplication

from app.util.tools import parse_args


class Trigger:
    enable = True
    as_last = False

    def __init__(self, message, *args):
        """根据需求可重写此构造方法"""
        self.msg: List[str] = parse_args(message.asDisplay())
        self.message: MessageChain = message
        for arg in args:
            if isinstance(arg, Friend):
                self.friend: Friend = arg  # 消息来源 好友
            elif isinstance(arg, Group):
                self.group: Group = arg  # 消息来源 群聊
            elif isinstance(arg, Member):
                self.member: Member = arg  # 群聊消息发送者
            elif isinstance(arg, GraiaMiraiApplication):
                self.app: GraiaMiraiApplication = arg  # 程序执行主体
        self.resp = None

    async def process(self):
        raise NotImplementedError

    async def do_send(self, resp):
        """发送消息"""
        if not isinstance(resp, MessageChain):
            return
        if hasattr(self, 'friend'):  # 发送好友消息
            await self.app.sendFriendMessage(self.friend, resp)
        elif hasattr(self, 'group'):  # 发送群聊消息
            await self.app.sendGroupMessage(self.group, resp)
