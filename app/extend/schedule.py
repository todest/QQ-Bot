import os

from graia import scheduler
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain
from graia.scheduler import timers
from graia.scheduler.timers import crontabify

from app.core.settings import ID_TO_GROUP, LISTEN_MC_SERVER
from app.extend.mc import mc_listener
from app.plugin.dujitang import DuJiTang
from app.util.tools import app_path


async def custom_schedule(loop, bcc, bot):
    sche = scheduler.GraiaScheduler(loop=loop, broadcast=bcc)

    @sche.schedule(crontabify('0 7 * * *'))
    async def every_day_dujitang():
        target = await bot.getGroup(ID_TO_GROUP[1])
        obj = DuJiTang(MessageChain.create([Plain('.jt')]), target)
        await obj.get_resp()
        await bot.sendGroupMessage(target, obj.resp)

    if not os.path.exists(path := os.sep.join([app_path(), 'tmp', 'mcserver'])):
        os.makedirs(path)
    for ips, qq, delay in LISTEN_MC_SERVER:
        @sche.schedule(timers.every_custom_seconds(delay))
        async def mc_listen_schedule():
            await mc_listener(bot, path, ips, qq, delay)
