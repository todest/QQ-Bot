import asyncio
import random

from graia.application import MessageChain, Friend
from graia.application.message.elements.internal import Plain, At, Face

from app.plugin.base import Plugin
from app.resource.earn_quot import *
from app.util.dao import MysqlDao
from app.util.tools import isstartswith


class BotUser:
    def __init__(self, qq, point=0):
        self.qq = qq
        self.point = point
        self.user_register()

    def user_register(self):
        """注册用户"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM user WHERE qq=%s",
                [self.qq]
            )
            if not res[0][0]:
                res = db.update(
                    "INSERT INTO user (qq, points) VALUES (%s, %s)",
                    [self.qq, self.point]
                )
                if not res:
                    raise Exception()

    def sign_in(self):
        """签到"""
        with MysqlDao() as db:
            res = db.update(
                "UPDATE user SET points=points+%s, last_login=CURDATE() WHERE qq=%s",
                [self.point, self.qq]
            )
            if not res:
                raise Exception()

    def update_point(self, point):
        """修改积分
        :param point: str, 积分变动值
        """
        with MysqlDao() as db:
            res = db.update(
                "UPDATE user SET points=points+%s WHERE qq=%s",
                [point, self.qq]
            )
            if not res:
                raise Exception()

    def get_sign_in_status(self) -> bool:
        """查询签到状态"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM user WHERE qq=%s AND last_login=CURDATE()",
                [self.qq]
            )
            return res[0][0]

    def get_points(self) -> bool:
        """查询积分"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT points FROM user WHERE qq=%s",
                [self.qq]
            )
            return res[0][0]

    def kick(self, src, dst, point, num) -> bool:
        """踢

            :param src: 来源QQ
            :param dst: 目标QQ
            :param point: 掉落积分
            :param num: 每天最多次数
        """
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM kick WHERE src=%s AND dst=%s AND TO_DAYS(time)=TO_DAYS(now())",
                [src, dst]
            )
            if not res[0][0] < num:
                return False
            self.update_point(point)
            res = db.update(
                "INSERT INTO kick (src, dst, time, point) VALUES (%s, %s, NOW(), %s)",
                [src, dst, -point]
            )
            if not res:
                raise Exception()
        return True

    def steal(self, src, dst, point, num) -> bool:
        """偷对方积分

            :param src: 来源QQ
            :param dst: 目标QQ
            :param point: 偷取积分
            :param num: 每天最多次数
        """
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM steal WHERE src=%s AND dst=%s AND TO_DAYS(time)=TO_DAYS(now())",
                [src, dst]
            )
            if not res[0][0] < num:
                return False
            self.update_point(point)
            res = db.update(
                "INSERT INTO steal (src, dst, time, point) VALUES (%s, %s, NOW(), %s)",
                [src, dst, point]
            )
            if not res:
                raise Exception()
        return True

    def bomb(self, src, dst, point, num) -> bool:
        """炸

            :param src: 来源QQ
            :param dst: 目标QQ
            :param point: 掉落积分
            :param num: 每天最多次数
        """
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM bomb WHERE src=%s AND dst=%s AND TO_DAYS(time)=TO_DAYS(now())",
                [src, dst]
            )
            if not res[0][0] < num:
                return False
            self.update_point(point)
            res = db.update(
                "INSERT INTO bomb (src, dst, time, point) VALUES (%s, %s, NOW(), %s)",
                [src, dst, point]
            )
            if not res:
                raise Exception()
        return True

    def get_moving_bricks_status(self) -> bool:
        """查询搬砖状态"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM user WHERE qq=%s AND last_moving_bricks=CURDATE()",
                [self.qq]
            )
            return res[0][0]

    def moving_bricks(self):
        """搬砖"""
        with MysqlDao() as db:
            res = db.update(
                "UPDATE user SET points=points+%s, last_moving_bricks=CURDATE() WHERE qq=%s",
                [self.point, self.qq]
            )
            if not res:
                raise Exception()

    def get_work_status(self) -> bool:
        """查询打工状态"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM user WHERE qq=%s AND last_part_time_job=CURDATE()",
                [self.qq]
            )
            return res[0][0]

    def work(self):
        """打工"""
        with MysqlDao() as db:
            res = db.update(
                "UPDATE user SET points=points+%s, last_part_time_job=CURDATE() WHERE qq=%s",
                [self.point, self.qq]
            )
            if not res:
                raise Exception()


class Game(Plugin):
    entry = ['.gp', '.积分']
    brief_help = '\r\n[√]\t积分：gp'
    full_help = \
        '.积分/.gp\t可以查询当前积分总量。\r\n' \
        '.积分/.gp 签到/signin\t每天可以签到随机获取积分。\r\n' \
        '.积分/.gp 搬砖/bz\t每天可以搬砖随机获取积分。\r\n' \
        '.积分/.gp 打工/work\t每天可以打工随机获取积分。\r\n' \
        '.积分/.gp 转给/tf@XX[num]\t转给XX num积分。\r\n' \
        '.积分/.gp 踢/kick@XX\t消耗10积分踢XX，使其掉落随机数量积分！\r\n' \
        '.积分/.gp 排行/rank\t显示群内已注册成员积分排行榜'

    num = {
        # c: cost, p: percent, d: drops, m: max
        'bomb': {'c': 10, 'p': 0.8, 'd': 30, 'm': 1},
        'kick': {'c': 30, 'p': 0.8, 'd': 60, 'm': 1},
        'steal': {'c': 50, 'p': 0.8, 'd': 100, 'm': 1},
    }

    async def process(self):
        if not self.msg:
            """查询积分"""
            try:
                user = BotUser((getattr(self, 'friend', None) or getattr(self, 'member', None)).id)
                point = user.get_points()
                if hasattr(self, 'group'):
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain(' 你的积分为%d!' % int(point))
                    ])
                else:
                    self.resp = MessageChain.create([
                        Plain(' 你的积分为%d!' % int(point))
                    ])
            except Exception as e:
                print(e)
                self.unkown_error()
            return
        if isstartswith(self.msg[0], ['签到', 'signin']):
            """签到"""
            try:
                point = random.randint(1, 101)
                user = BotUser((getattr(self, 'friend', None) or getattr(self, 'member', None)).id, point)
                if user.get_sign_in_status():
                    if hasattr(self, 'group'):
                        self.resp = MessageChain.create([
                            At(self.member.id),
                            Plain(' 你今天已经签到过了！'),
                        ])
                    else:
                        self.resp = MessageChain.create([
                            Plain(' 你今天已经签到过了！')
                        ])
                else:
                    user.sign_in()
                    if hasattr(self, 'group'):
                        self.resp = MessageChain.create([
                            At(self.member.id),
                            Plain(' 签到成功，%s获得%d积分' % (
                                '运气爆棚！' if point >= 90 else '', point
                            )),
                        ])
                    else:
                        self.resp = MessageChain.create([
                            Plain(' 签到成功，%s获得%d积分' % (
                                '运气爆棚！' if point >= 90 else '', point
                            )),
                        ])
            except Exception as e:
                print(e)
                self.unkown_error()
        elif isstartswith(self.msg[0], ['转给', '转账', 'tf']):
            """转账"""
            try:
                if len(self.msg) == 1:
                    self.args_error()
                    return
                point = int(self.msg[1])
                if point <= 0:
                    self.args_error()
                    return
                user = BotUser((getattr(self, 'friend', None) or getattr(self, 'member', None)).id)
                if int(user.get_points()) < point:
                    self.point_not_enough()
                    return
                target = self.message.get(At)[0]
                if not target:
                    self.args_error()
                    return
                user.update_point(-point)
                user = BotUser(target.dict()['target'], point)
                user.update_point(point)
                self.resp = MessageChain.create([
                    At(self.member.id),
                    Plain(' 已转赠给'),
                    target,
                    Plain(' %d积分！' % point)
                ])
            except ValueError as e:
                print(e)
                self.arg_type_error()
            except Exception as e:
                print(e)
                self.unkown_error()
        elif isstartswith(self.msg[0], ['踢', 'kick']):
            """踢"""
            try:
                target = self.message.get(At)

                # 判断是否有At，如果无，要求报错并返回
                if not target:
                    self.args_error()
                    return
                target = target[0]
                the_one = BotUser(self.member.id)

                # 判断积分是否足够，如果无，要求报错并返回
                if int(the_one.get_points()) < self.num['kick']['c']:
                    self.point_not_enough()
                    return

                # 判断被踢者是否有积分，如果无，要求回执
                the_other = BotUser(target.dict()['target'])
                rest = int(the_other.get_points())
                if rest <= 0:
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain(' 对方是个穷光蛋！请不要伤害他！')
                    ])
                    return

                # 判断踢次数上限
                status = the_one.kick(
                    self.member.id, target.dict()['target'],
                    -self.num['kick']['c'],
                    self.num['kick']['m']
                )
                if not status:
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain(' 你今天踢对方次数已达上限，请明天再来！')
                    ])
                    return

                # 随机掉落积分
                point = random.randint(0, min(int(self.num['kick']['p'] * rest), self.num['kick']['d']))
                if point:
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain(' 花费%d积分踢了' % self.num['kick']['c']),
                        target,
                        Plain(' 一脚，对方掉了%d积分，对你骂骂咧咧' % point),
                        Face(faceId=31),
                        Plain('！')
                    ])
                    the_other.update_point(-point)
                else:
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain(' 花费%d积分踢了' % self.num['kick']['c']),
                        target,
                        Plain(' 一脚，对方没有掉落积分，对你做了个鬼脸'),
                        Face(faceId=286),
                        Plain('！')
                    ])

            except Exception as e:
                print(e)
                self.unkown_error()
        # elif isstartswith(self.msg[0], ['炸', 'bomb']):
        # 	try:
        # 		target = self.message.get(At)
        #
        # 		# 判断是否有At，如果无，要求报错并返回
        # 		if not target:
        # 			self.args_error()
        # 			return
        # 		target = target[0]
        # 		the_one = BotUser(self.member.id)
        #
        # 		# 判断被踢者是否有积分，如果无，要求回执
        # 		the_other = BotUser(target.dict()['target'])
        # 		rest = int(the_other.get_points())
        #
        # 		if rest <= 0:
        # 			self.resp = MessageChain.create([
        # 				At(self.member.id),
        # 				Plain(' 砰，炸弹爆炸了，'),
        # 				target,
        # 				Plain(' 被炸飞了，但什么也没剩下！')
        # 			])
        # 			return
        #
        # 	except Exception as e:
        # 		print(e)
        # 		self.unkown_error()
        elif isstartswith(self.msg[0], ['偷', 'steal']):
            try:
                target = self.message.get(At)

                # 判断是否有At，如果无，要求报错并返回
                if not target:
                    self.args_error()
                    return
                target = target[0]
                the_one = BotUser(self.member.id)

                # 判断被踢者是否有积分，如果无，要求回执
                the_other = BotUser(target.dict()['target'])
                rest = int(the_other.get_points())

                if rest <= 0:
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain(' 你摸遍了他全身也没找到一点东西！')
                    ])
                    return

                point = random.randint(0, min(int(self.num['steal']['p'] * rest), self.num['steal']['d']))
                status = the_one.steal(self.member.id, target.dict()['target'], point, self.num['steal']['m'])
                if not status:
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain(' 你今天偷对方次数已达上限，请明天再来！')
                    ])
                    return
                if point:
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain(' 你趁'),
                        target,
                        Plain(' 不注意，偷了对方%d积分！' % point)
                    ])
                    the_other.update_point(-point)
                else:
                    self.resp = MessageChain.create([
                        At(self.member.id),
                        Plain('你什么也没偷到！')
                    ])

            except Exception as e:
                print(e)
                self.unkown_error()
        elif isstartswith(self.msg[0], ['搬砖', 'bz']):
            try:
                point = random.randint(40, 81)
                user = BotUser((getattr(self, 'friend', None) or getattr(self, 'member', None)).id, point)
                if user.get_moving_bricks_status():
                    if hasattr(self, 'group'):
                        self.resp = MessageChain.create([
                            At(self.member.id),
                            Plain(' '),
                            Plain(random.choice(bricks_done))
                        ])
                    else:
                        self.resp = MessageChain.create([
                            Plain(random.choice(bricks_done))
                        ])
                else:
                    user.moving_bricks()
                    if hasattr(self, 'group'):
                        self.resp = MessageChain.create([
                            At(self.member.id),
                            Plain(' 你搬了一天砖，获得%d积分！' % point),
                            Plain(random.choice(bricks))
                        ])
                    else:
                        self.resp = MessageChain.create([
                            Plain(' 你搬了一天砖，获得%d积分！' % point),
                            Plain(random.choice(bricks))
                        ])
            except Exception as e:
                print(e)
                self.unkown_error()
        elif isstartswith(self.msg[0], ['打工', 'work']):
            try:
                point = random.randint(100, 181)
                user = BotUser((getattr(self, 'friend', None) or getattr(self, 'member', None)).id, point)
                if user.get_work_status():
                    if hasattr(self, 'group'):
                        self.resp = MessageChain.create([
                            At(self.member.id),
                            Plain(' '),
                            Plain(random.choice(works_done))
                        ])
                    else:
                        self.resp = MessageChain.create([
                            Plain(random.choice(works_done))
                        ])
                else:
                    user.work()
                    if hasattr(self, 'group'):
                        self.resp = MessageChain.create([
                            At(self.member.id),
                            Plain(' 你打了一天工，获得%d积分！' % point),
                            Plain(random.choice(works))
                        ])
                    else:
                        self.resp = MessageChain.create([
                            Plain(' 你打了一天工，获得%d积分！' % point),
                            Plain(random.choice(works))
                        ])
            except Exception as e:
                print(e)
                self.unkown_error()
        elif isstartswith(self.msg[0], ['排行', 'rank']):
            try:
                with MysqlDao() as db:
                    res = db.query(
                        "SELECT qq, points FROM user ORDER BY points DESC"
                    )
                    members = await self.app.memberList(self.group.id)
                    group_user = {item.id: item.name for item in members}
                    self.resp = MessageChain.create([Plain('群内积分排行：\r\n')])
                    index = 1
                    for item in res:
                        if int(item[0]) in group_user.keys():
                            self.resp.plus(
                                MessageChain.create([Plain(
                                    '%d. ' % index + group_user[int(item[0])] + ': %d\r\n' % item[1]
                                )])
                            )
                            index += 1
            except Exception as e:
                print(e)
                self.unkown_error()
        else:
            self.args_error()


if __name__ == '__main__':
    a = Game(MessageChain.create([Plain('.积分')]), Friend.construct(id=123))
    asyncio.run(a.get_resp())
    print(a.resp)
