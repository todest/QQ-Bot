import pymysql
from app.core.settings import *


class MysqlDao:
	def __enter__(self):
		try:
			self.db = pymysql.connect(
				host=LOGIN_HOST,
				user=MYSQL_USER,
				password=MYSQL_PWD,
				database='bot'
			)
			self.cur = self.db.cursor()
			return self
		except Exception as e:
			print(e)
			raise e

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.cur.close()
		self.db.close()

	def query(self, sql, args=None):
		try:
			self.cur.execute(sql, args=args)
			query_result = self.cur.fetchall()
		except Exception as e:
			print(e)
			raise e
		return query_result

	def update(self, sql):
		effect_rows = 0
		try:
			effect_rows = self.cur.execute(sql)
			self.db.commit()
		except Exception as e:
			self.db.rollback()
			print(e)
			raise e
		return effect_rows


if __name__ == '__main__':
	with MysqlDao() as db:
		res = db.query('select * from user')
		print(res)
