import subprocess

from graia.application import MessageChain
from graia.application.message.elements.internal import At, Plain

from app.plugin.base import Plugin
from app.util.decorator import permission_required
from app.util.tools import isstartswith, app_path


class Admin(Plugin):
    entry = ['.power', '.电源', '.p']
    brief_help = '\r\n[√]\t电源：p'
    full_help = \
        '.电源/.p\t仅限管理员使用！\r\n' \
        '.电源/.p k\t关闭机器人\r\n' \
        '.电源/.p r\t重启机器人\r\n' \
        '.电源/.p u [timeout]\t升级机器人(默认超时时间为10秒)\r\n'
    hidden = True

    @permission_required(level='ADMIN')
    async def process(self):
        if not self.msg:
            self.print_help()
            return
        try:
            if isstartswith(self.msg[0], ['k', 'u', 'r']):
                if hasattr(self, 'group'):
                    subprocess.call(f'./run.sh -g {self.group.id} -t {self.member.id}', cwd=app_path(), shell=True)
                elif hasattr(self, 'friend'):
                    subprocess.call(f'./run.sh -t {self.member.id}', cwd=app_path(), shell=True)
                if isstartswith(self.msg[0], 'k'):
                    subprocess.call(f'./run.sh -k', cwd=app_path(), shell=True)
                elif isstartswith(self.msg[0], 'u'):
                    timeout = 10
                    if len(self.msg) == 2 and self.msg[1].isdigit():
                        timeout = int(self.msg[1])
                    try:
                        subprocess.call(f'./run.sh -u', timeout=timeout, cwd=app_path(), shell=True)
                    except subprocess.TimeoutExpired:
                        if hasattr(self, 'group'):
                            self.resp = MessageChain.create([
                                At(self.member.id),
                                Plain(" 升级超时！")
                            ])
                        else:
                            self.resp = MessageChain.create([
                                Plain("升级超时！")
                            ])
                elif isstartswith(self.msg[0], 'r'):
                    subprocess.call(f'./run.sh -r', cwd=app_path(), shell=True)
            else:
                self.args_error()
                return
        except Exception as e:
            print(e)
            self.unkown_error()
