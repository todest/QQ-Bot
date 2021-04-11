from graia import scheduler
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain
from graia.scheduler import timers
from graia.scheduler.timers import crontabify

from app.core.settings import ID_TO_GROUP
from app.extend.mc import mc_listener
from app.plugin.dujitang import DuJiTang


async def custom_schedule(loop, bcc, bot):
    sche = scheduler.GraiaScheduler(loop=loop, broadcast=bcc)

    @sche.schedule(crontabify('0 7 * * *'))
    async def every_day_dujitang():
        target = await bot.getGroup(ID_TO_GROUP[1])
        obj = DuJiTang(MessageChain.create([Plain('.jt')]), target)
        await obj.get_resp()
        await bot.sendGroupMessage(target, obj.resp)

    dalay_sec = 10

    @sche.schedule(timers.every_custom_seconds(dalay_sec))
    async def mc_listen_schedule():
        await mc_listener(bot, dalay_sec)
