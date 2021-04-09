from graia import scheduler
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain
from graia.scheduler.timers import crontabify

from app.core.settings import ID_TO_GROUP
from app.plugin.dujitang import DuJiTang


async def custom_schedule(loop, bcc, bot):
    sche = scheduler.GraiaScheduler(loop=loop, broadcast=bcc)

    @sche.schedule(crontabify('0 7 * * *'))
    async def every_day_dujitang():
        target = await bot.getGroup(ID_TO_GROUP[1])
        obj = DuJiTang(MessageChain.create([Plain('.jt')]), target)
        await obj.get_resp()
        await bot.sendGroupMessage(target, obj.resp)
