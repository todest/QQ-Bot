from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from app.core.settings import ACTIVE_USER
from app.plugin.base import Plugin
from app.util.decorator import permission_required


class Test(Plugin):
    entry = ['.test']
    brief_help = '\r\n[√]\t测试：test'
    full_help = '仅限测试使用！'
    enable = True
    hidden = True

    @permission_required(level='ADMIN')
    async def process(self):
        if not self.msg:
            self.print_help()
            return
