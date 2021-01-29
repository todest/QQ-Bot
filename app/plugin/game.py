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
		'.积分 签到\t每天可以签到随机获取积分，积分值从0-100不等。\r\n'

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
				point = random.randint(0, 101)
				user = User(self.source.id, point)
				if user.get_sign_in_status():
					if isinstance(self.source, Member):
						self.resp = MessageChain.create([
							At(self.source.id),
							Plain(' 你今天已经签到过了！'),
						])
					else:
						self.resp = MessageChain.create([
							Plain(' 你今天已经签到过了！'),
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
		else:
			self.args_error()


if __name__ == '__main__':
	a = Game('.游戏 积分', Member.construct(id=123))
	print(a.get_resp())
