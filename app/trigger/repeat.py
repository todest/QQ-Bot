import random

from app.trigger.trigger import Trigger
from app.util.msg import repeated, save


class Repeat(Trigger):
    async def process(self):
        if not hasattr(self, 'group'):
            return
        probability = random.randint(0, 101)
        if (probability < 1) and repeated(self.group.id, self.app.connect_info.account, 2):
            await self.app.sendGroupMessage(self.group, self.message.asSendable())
            save(self.group.id, self.app.connect_info.account, self.message.asDisplay())
            self.app.logger.info('Random Repeat: ' + self.message.asDisplay())
        if repeated(self.group.id, self.app.connect_info.account, 2):
            await self.app.sendGroupMessage(self.group, self.message.asSendable())
            save(self.group.id, self.app.connect_info.account, self.message.asDisplay())
            self.app.logger.info('Follow Repeat: ' + self.message.asDisplay())
