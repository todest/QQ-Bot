import os
import pickle
import time

import jsonpath
from graia.application import MessageChain, enter_context
from graia.application.message.elements.internal import Plain

from app.core.settings import *
from app.plugin.mcinfo import StatusPing
from app.util.tools import app_path


class McServer:
    status = False
    players = set()
    description = ''

    def __init__(self, default_ip='127.0.0.1', default_port=25565):
        self.ip = default_ip
        self.port = default_port
        self.update(init=True)
        self.time = time.time()

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
            self.time = time.time()
            if resp_content.__root__:
                resp.plus(resp_content)
                return resp
            return None


async def mc_listener(app, delay_sec):
    if not LISTEN_MC_SERVER:
        return
    if not os.path.exists(path := os.sep.join([app_path(), 'tmp', 'mcserver'])):
        os.makedirs(path)
    for ips, qq, _ in LISTEN_MC_SERVER:
        if os.path.exists(file := os.sep.join([path, f'{ips[0]}_{str(ips[1])}.dat'])):
            with open(file, 'rb') as f:
                obj = pickle.load(f)
        else:
            obj = McServer(*ips)
        if time.time() - obj.time > int(1.5 * delay_sec):
            obj = McServer(*ips)
        resp = obj.update()
        with open(file, 'wb') as f:
            pickle.dump(obj, f)
        if not resp:
            continue
        for target in qq:
            target = await app.getFriend(target)
            if not target:
                continue
            await app.sendFriendMessage(target, resp)
