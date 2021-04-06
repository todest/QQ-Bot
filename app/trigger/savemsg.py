from app.trigger.trigger import Trigger
from app.util.msg import save


class SaveMsg(Trigger):
    async def process(self):
        if not hasattr(self, 'group'):
            return
        save(self.group.id, self.member.id, self.message.asDisplay())
