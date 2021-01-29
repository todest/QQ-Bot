import time
import random

from app.util.dao import MysqlDao
from app.plugin.base import Plugin
from graia.application import MessageChain, Member

from graia.application.message.elements.internal import Plain, At


class User:
	def __init__(self, qq, point=0):
		self.qq = qq
		self.point = point
		self.date = int(time.strftime('%Y%m%d', time.localtime()))
		self.exist = self._user_exist_check()

	def _user_exist_check(self):
		"""查询用户是否存在"""
		with MysqlDao() as db:
			res = db.query(
				"SELECT COUNT(*) FROM user WHERE qq='{}'".format(
					self.qq
				))
			return res[0][0]

	def sign_in(self):
		"""签到"""
		if self.exist:
			with MysqlDao() as db:
				res = db.update(
					"UPDATE user SET points=points+{}, last_login={} WHERE qq='{}'".format(
						self.point, self.date, self.qq
					))
				if not res:
					raise Exception()
		else:
			with MysqlDao() as db:
				res = db.update(
					"INSERT INTO user (qq, points, last_login) VALUES ('{}', {}, {})".format(
						self.qq, self.point, self.date
					))
				if not res:
					raise Exception()

	def set_point(self, point):
		"""修改积分"""
		if self.exist:
			with MysqlDao() as db:
				res = db.update(
					"UPDATE user SET points=points+{} WHERE qq='{}'".format(
						point, self.qq
					))
				if not res:
					raise Exception()
		else:
			with MysqlDao() as db:
				res = db.update(
					"INSERT INTO user (qq, points) VALUES ('{}', {})".format(
						self.qq, point
					))
				if not res:
					raise Exception()

	def get_sign_in_status(self):
		"""查询签到状态"""
		if self.exist:
			with MysqlDao() as db:
				res = db.query(
					"SELECT last_login FROM user WHERE qq='{}'".format(
						self.qq
					))
				if str(res[0][0]).replace('-', '') == str(self.date):
					return True
		return False

	def get_points(self):
		if self.exist:
			with MysqlDao() as db:
				res = db.query(
					"SELECT points FROM user WHERE qq='{}'".format(
						self.qq
					)
				)
				return res[0][0]
		else:
			return 0


class Game(Plugin):
	entry = '.积分'
	brief_help = entry + '\t积分专区\r\n'
	full_help = \
		'.积分\t可以查询当前积分总量。\r\n' \
		'.积分 签到\t每天可以签到随机获取积分。\r\n' \
		'.积分 转给@XX[num]\t转给XX num积分。\r\n' \
		'.积分 踢@XX\t消耗10积分踢XX，使其掉落随机数量积分！\r\n'

	def process(self):
		if not self.msg:
			try:
				user = User(self.source.id)
				point = user.get_points()
				if isinstance(self.source, Member):
					self.resp = MessageChain.create([
						At(self.source.id),
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
		if self.msg[0].startswith('签到'):
			try:
				point = random.randint(1, 101)
				user = User(self.source.id, point)
				if user.get_sign_in_status():
					if isinstance(self.source, Member):
						self.resp = MessageChain.create([
							At(self.source.id),
							Plain(' 你今天已经签到过了！'),
						])
					else:
						self.resp = MessageChain.create([
							Plain(' 你今天已经签到过了！')
						])
				else:
					user.sign_in()
					if isinstance(self.source, Member):
						self.resp = MessageChain.create([
							At(self.source.id),
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
		elif self.msg[0].startswith('转给'):
			try:
				if len(self.msg) == 1:
					self.args_error()
					return
				point = int(self.msg[1])
				if point <= 0:
					self.args_error()
					return
				user = User(self.source.id)
				if int(user.get_points()) < point:
					self.point_not_enough()
					return
				target = self.message.get(At)[0]
				if not target:
					self.args_error()
					return
				user.set_point(-point)
				user = User(target.dict()['target'], point)
				user.set_point(point)
				self.resp = MessageChain.create([
					At(self.source.id),
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
		elif self.msg[0].startswith('踢'):
			target = self.message.get(At)[0]
			if not target:
				self.args_error()
				return
			user1 = User(self.source.id)
			if int(user1.get_points()) < 10:
				self.point_not_enough()
				return
			user2 = User(target.dict()['target'])
			rest = int(user2.get_points())
			point = random.randint(0, int(0.8 * rest))
			if rest <= 0:
				self.resp = MessageChain.create([
					At(self.source.id),
					Plain(' 对方是个穷光蛋！请不要伤害他！')
				])
				return
			user1.set_point(-10)
			if rest <= point:
				point = rest
				self.resp = MessageChain.create([
					At(self.source.id),
					Plain(' 花费10积分踢了'),
					target,
					Plain('一脚，对方掉了%d积分，变成了穷光蛋！' % rest)
				])
			else:
				self.resp = MessageChain.create([
					At(self.source.id),
					Plain(' 花费10积分踢了'),
					target,
					Plain('一脚，对方掉了%d积分，对你咬牙切齿！' % point)
				])
			if point:
				user2.set_point(-point)
		else:
			self.args_error()


if __name__ == '__main__':
	a = Game('.游戏 积分', Member.construct(id=123))
	print(a.get_resp())
