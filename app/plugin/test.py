from app.plugin.base import Plugin


class Test(Plugin):
    entry = ['.test']
    brief_help = '\r\n[√]\t测试：test'
    full_help = '仅限测试使用！'
    enable = True
    hidden = True

    async def process(self):
        if not self.check_admin():
            return
