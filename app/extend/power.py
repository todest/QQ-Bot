import getopt

from graia.application import MessageChain
from graia.application.message.elements.internal import Plain, At

from app.core.settings import *


async def power(app, argv):
    upgrade_failure = False
    shutdown_failure = False
    command_from_group = False
    reboot_success = False
    command_executor = await app.getFriend(ADMIN_USER[0])
    try:
        opts, args = getopt.getopt(argv[1:], "ru:k:g:e:", ["r", "u=", "k=", "g=", "e="])
    except getopt.GetoptError:
        await app.sendFriendMessage(command_executor, MessageChain.create([Plain("脚本参数错误")]))
        return
    for opt, arg in opts:
        if opt == '-h':
            await app.sendFriendMessage(command_executor, MessageChain.create([
                Plain("这是帮助菜单！")
            ]))
            return
        elif opt in ('-u', '--upgrade'):
            upgrade_failure = arg
        elif opt in ('-k', '--kill'):
            shutdown_failure = arg
        elif opt in ('-r', '--reboot'):
            reboot_success = True
        elif opt in ('-g', '--group'):
            command_from_group = await app.getGroup(command_from_group)
        elif opt in ('-e', '--executor'):
            command_executor = await app.getFriend(arg)
    if shutdown_failure:
        if command_from_group:
            await app.sendGroupMessage(command_from_group, [
                At(command_executor),
                Plain(' 进程未正常结束！')
            ])
        else:
            await app.sendFriendMessage(command_executor, MessageChain([
                Plain('进程未正常结束！')
            ]))
    if upgrade_failure:
        if command_from_group:
            await app.sendGroupMessage(command_from_group, [
                At(command_executor),
                Plain(' 升级失败！')
            ])
        else:
            await app.sendFriendMessage(command_executor, MessageChain([
                Plain('升级失败！')
            ]))
    else:
        if command_from_group:
            await app.sendGroupMessage(command_from_group, [
                At(command_executor),
                Plain(' 升级成功！')
            ])
        else:
            await app.sendFriendMessage(command_executor, MessageChain([
                Plain('升级成功！')
            ]))
    if reboot_success:
        if command_from_group:
            await app.sendGroupMessage(command_from_group, [
                At(command_executor),
                Plain(' 重启成功！')
            ])
        else:
            await app.sendFriendMessage(command_executor, MessageChain([
                Plain('重启成功！')
            ]))
