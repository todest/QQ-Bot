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
    description = None

    def __init__(self, ip='127.0.0.1', port=25565):
        self.ip = ip
        self.port = port
        self.update(init=True)

    def update(self, init=False):
        players = self.players.copy()
        description = self.description
        # noinspection PyBroadException
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
        except Exception:
            status = False
            players.clear()

        if init:
            self.status = status
            self.players = players
            self.description = description
        else:
            resp_player = MessageChain.create([])
            if players != self.players:
                for player in self.players - players:
                    resp_player.plus(MessageChain.create([
                        Plain('%s退出了%s:%d（%s）MC服务器！\r\n' % (player, self.ip, self.port, self.description))
                    ]))
                for player in players - self.players:
                    resp_player.plus(MessageChain.create([
                        Plain('%s加入了%s:%d（%s）MC服务器！\r\n' % (player, self.ip, self.port, self.description))
                    ]))
                self.players = players
            else:
                resp_player = None

            resp_server = MessageChain.create([])
            if status != self.status:
                if status:
                    resp_server.plus(MessageChain.create([
                        Plain('MC服务器%s:%d（%s）已开启！' % (self.ip, self.port, self.description))
                    ]))
                else:
                    resp_server.plus(MessageChain.create([
                        Plain('MC服务器%s:%d（%s）已关闭！' % (self.ip, self.port, self.description))
                    ]))
                self.status = status
            else:
                resp_server = None

            if resp_server:
                if status:
                    return resp_server, resp_player
                else:
                    return resp_player, resp_server
            else:
                return resp_player, None
        return None, None


async def mc_listener(app):
    data = []
    for ips, qq in LISTEN_MC_SERVER:
        data.append([McServer(*ips), qq])
    while True:
        for item, qq in data:
            resp_a, resp_b = item.update()
            if not resp_a:
                continue
            for target in qq:
                target = await app.getFriend(target)
                if not target:
                    continue
                with enter_context(app=app):
                    await app.sendFriendMessage(target, resp_a)
                    if resp_b:
                        await app.sendFriendMessage(target, resp_b)
        await asyncio.sleep(60)
