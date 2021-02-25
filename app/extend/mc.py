import asyncio

import jsonpath
from graia.application import MessageChain
from graia.application.context import enter_context
from graia.application.message.elements.internal import Plain

from app.core.settings import *
from app.plugin.mcinfo import StatusPing


class McServer:
    status = False
    players = set()
    description = ''

    def __init__(self, ip='127.0.0.1', port=25565):
        self.ip = ip
        self.port = port
        self.update(init=True)

    def update(self, init=False):
        players = self.players.copy()
        description = self.description
        try:
            response = StatusPing(self.ip, self.port).get_status()
            status = True
            names = jsonpath.jsonpath(response, '$..sample[..name]')
            description = jsonpath.jsonpath(response, '$..description')[0]
            if jsonpath.jsonpath(description, '$..text'):
                description = jsonpath.jsonpath(description, '$..text')[-1]
            if names:
                for index in range(len(names)):
                    players.update({names[index]})
            else:
                players.clear()
        except (EnvironmentError, Exception):
            status = False
            players.clear()

        if init:
            self.status = status
            self.players = players
            self.description = description
        else:
            resp = MessageChain.create([
                Plain(f'地址：{self.ip}:{self.port}\r\n'),
                Plain(f'描述：{description}\r\n'),
                Plain(f'信息：\r\n')
            ])
            resp_content = MessageChain.create([])
            if status and (status != self.status):
                resp_content.plus(MessageChain.create([
                    Plain('服务器已开启！\r\n')
                ]))
            for player in self.players - players:
                resp_content.plus(MessageChain.create([
                    Plain(f'{player}退出了服务器！\r\n')
                ]))
            for player in players - self.players:
                resp_content.plus(MessageChain.create([
                    Plain(f'{player}加入了服务器！\r\n')
                ]))
            if (not status) and (status != self.status):
                resp_content.plus(MessageChain.create([
                    Plain('服务器已关闭！\r\n')
                ]))
            self.status = status
            self.players = players
            self.description = description
            if resp_content.__root__:
                resp.plus(resp_content)
                return resp
            return None


async def mc_listener(app):
    data = []
    for ips, qq in LISTEN_MC_SERVER:
        data.append([McServer(*ips), qq])
    while True:
        await asyncio.sleep(LISTEN_DELAY)
        app.logger.info('mc_listener is running...')
        for item, qq in data:
            resp = item.update()
            if not resp:
                continue
            for target in qq:
                target = await app.getFriend(target)
                if not target:
                    continue
                with enter_context(app=app):
                    await app.sendFriendMessage(target, resp)
