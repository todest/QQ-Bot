import asyncio
import time
import random
from app.util.dao import MysqlDao
from app.plugin.base import Plugin
from app.util.tools import isstartswith
from graia.application import MessageChain, Member, Friend
from graia.application.message.elements.internal import Plain, At, Face


class BotUser:
	def __init__(self, qq, point=0):
		self.qq = qq
		self.point = point
		self.date = int(time.strftime('%Y%m%d', time.localtime()))
		self.exist = self._user_exist_check()

	def _user_exist_check(self):
		"""查询用户是否存在"""
		with MysqlDao() as db:
			res = db.query(
				"SELECT COUNT(*) FROM user WHERE qq=%s",
				[self.point]
			)
			return res[0][0]

	def sign_in(self):
		"""签到"""
		if self.exist:
			with MysqlDao() as db:
				res = db.update(
					"UPDATE user SET points=points+%s, last_login=%s WHERE qq=%s",
					[self.point, self.date, self.qq]
				)
				if not res:
					raise Exception()
		else:
			with MysqlDao() as db:
				res = db.update(
					"INSERT INTO user (qq, points, last_login) VALUES (%s, %s, %s)",
					[self.qq, self.point, self.date]
				)
				if not res:
					raise Exception()

	def set_point(self, point):
		"""修改积分
		:param point: str, 积分变动值
		"""
		if self.exist:
			with MysqlDao() as db:
				res = db.update(
					"UPDATE user SET points=points+%s WHERE qq=%s",
					[point, self.qq]
				)
				if not res:
					raise Exception()
		else:
			with MysqlDao() as db:
				res = db.update(
					"INSERT INTO user (qq, points) VALUES (%s, %s)",
					[self.qq, point]
				)
				if not res:
					raise Exception()

	def get_sign_in_status(self):
		"""查询签到状态"""
		if self.exist:
			with MysqlDao() as db:
				res = db.query(
					"SELECT last_login FROM user WHERE qq=%s",
					[self.qq]
				)
				if str(res[0][0]).replace('-', '') == str(self.date):
					return True
		return False

	def get_points(self):
		"""查询积分"""
		if self.exist:
			with MysqlDao() as db:
				res = db.query(
					"SELECT points FROM user WHERE qq=%s",
					[self.qq]
				)
				return res[0][0]
		else:
			return 0


class Game(Plugin):
	entry = ['.gp', '.积分']
	brief_help = entry[0] + '\t积分专区\r\n'
	full_help = \
		'.积分/.gp\t可以查询当前积分总量。\r\n' \
		'.积分/.gp 签到/signin\t每天可以签到随机获取积分。\r\n' \
		'.积分/.gp 转给/tf@XX[num]\t转给XX num积分。\r\n' \
		'.积分/.gp 踢/kick@XX\t消耗10积分踢XX，使其掉落随机数量积分！\r\n' \
		'.积分/.gp 排行/rank\t显示群内已注册成员积分排行榜'

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
				user.set_point(-point)
				user = BotUser(target.dict()['target'], point)
				user.set_point(point)
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
				target = self.message.get(At)[0]

				# 判断是否有At，如果无，要求报错并返回
				if not target:
					self.args_error()
					return
				the_one = BotUser(self.member.id)

				# 判断积分是否足够，如果无，要求报错并返回
				if int(the_one.get_points()) < 10:
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

				# 随机掉落积分
				point = random.randint(0, min(int(0.8 * rest), 25))
				the_one.set_point(-10)
				if rest <= point:
					self.resp = MessageChain.create([
						At(self.member.id),
						Plain(' 花费10积分踢了'),
						target,
						Plain(' 一脚，对方掉了%d积分，变成了穷光蛋！' % rest)
					])
					the_other.set_point(-rest)
				else:
					if point:
						self.resp = MessageChain.create([
							At(self.member.id),
							Plain(' 花费10积分踢了'),
							target,
							Plain(' 一脚，对方掉了%d积分，对你骂骂咧咧' % point),
							Face(faceid=31),  # ZHOU_MA
							Plain('！')
						])
						the_other.set_point(-point)
					else:
						self.resp = MessageChain.create([
							At(self.member.id),
							Plain(' 花费10积分踢了'),
							target,
							Plain(' 一脚，对方没有掉落积分，对你做了个鬼脸'),
							Face(name='MO_GUI_XIAO'),  # 286
							Plain('！')
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
