import asyncio
import sys

from graia.application import GraiaMiraiApplication, Session
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.broadcast import Broadcast

from app.core.config import Config
from app.core.controller import Controller
from app.extend.mc import mc_listener
from app.extend.power import power
from app.extend.schedule import custom_schedule

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
config = Config()
bot = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host='http://' + config.LOGIN_HOST + ':' + config.LOGIN_PORT,
        authKey=config.AUTH_KEY,
        account=config.LOGIN_QQ,
        websocket=True
    )
)


@bcc.receiver("FriendMessage")
async def friend_message_listener(message: MessageChain, friend: Friend, app: GraiaMiraiApplication):
    event = Controller(message, friend, app)
    await event.process_event()


@bcc.receiver("GroupMessage")
async def group_message_listener(message: MessageChain, group: Group, member: Member, app: GraiaMiraiApplication):
    event = Controller(message, group, member, app)
    await event.process_event()


asyncio.run(custom_schedule(loop, bcc, bot))
loop.create_task(mc_listener(bot))
loop.create_task(power(bot, sys.argv))
bot.launch_blocking()
