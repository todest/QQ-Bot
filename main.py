from app.core.settings import *
from app.core.controller import Controller
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
bot = GraiaMiraiApplication(
	broadcast=bcc,
	connect_info=Session(
		host=LOGIN_HOST + ':' + LOGIN_PORT,
		authKey=AUTH_KEY,
		account=LOGIN_QQ,
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


bot.launch_blocking()
