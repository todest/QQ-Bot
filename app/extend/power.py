import getopt

from graia.application import MessageChain
from graia.application.message.elements.internal import Plain, At

from app.core.settings import *


async def power(app, argv):
    upgrade = False
    shutdown = False
    group = False
    reboot = False
    executor = await app.getFriend(ADMIN_USER[0])
    try:
        opts, args = getopt.getopt(argv[1:], '-r-k-u:-g:-e:', ['reboot', 'kill', 'upgrade=', 'group=', 'executor='])
    except getopt.GetoptError:
        await app.sendFriendMessage(executor, MessageChain.create([Plain("脚本参数错误")]))
        return
    for opt, arg in opts:
        if opt == '-h':
            await app.sendFriendMessage(executor, MessageChain.create([
                Plain('\t-r\t--reboot\t重启成功\r\n'),
                Plain('\t-k\t--kill\t关闭失败\r\n'),
                Plain('\t-u\t--upgrade\t升级状态\r\n'),
                Plain('\t\t例如：-u true, --group=true\r\n'),
                Plain('\t-g\t--group\t来自群组\r\n'),
                Plain('\t\t例如：-g 123, --group=123\r\n'),
                Plain('\t-e\t--executor\t执行者\r\n'),
                Plain('\t\t例如：-e 123, --e=123\r\n'),
            ]))
            return
        elif opt in ('-r', '--reboot'):
            reboot = True
        elif opt in ('-k', '--kill'):
            shutdown = True
        elif opt in ('-u', '--upgrade'):
            upgrade = True
        elif opt in ('-g', '--group'):
            group = await app.getGroup(group)
        elif opt in ('-e', '--executor'):
            executor = await app.getFriend(arg)
    if shutdown:
        if group:
            await app.sendGroupMessage(group, MessageChain.create([
                At(executor),
                Plain(' 进程未正常结束！')
            ]))
        else:
            await app.sendFriendMessage(executor, MessageChain.create([
                Plain('进程未正常结束！')
            ]))
    if upgrade:
        if group:
            await app.sendGroupMessage(group, [
                At(executor),
                Plain(' 升级失败！')
            ])
        else:
            await app.sendFriendMessage(executor, MessageChain.create([
                Plain('升级失败！')
            ]))
    else:
        if group:
            await app.sendGroupMessage(group, [
                At(executor),
                Plain(' 升级成功！')
            ])
        else:
            await app.sendFriendMessage(executor, MessageChain.create([
                Plain('升级成功！')
            ]))
    if reboot:
        if group:
            await app.sendGroupMessage(group, [
                At(executor),
                Plain(' 重启成功！')
            ])
        else:
            await app.sendFriendMessage(executor, MessageChain.create([
                Plain('重启成功！')
            ]))
