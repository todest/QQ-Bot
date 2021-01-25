import time
import math
import random


def f(x, mul, sigma):
	return 5000 * (1.0 / (math.sqrt(2 * math.pi) * sigma) * (math.e ** (-(x - mul) ** 2 / (2 * sigma * sigma))))


class Jrrp:
	def __init__(self, cid):
		self.id = str(cid)
		self.date = time.strftime("%Y%m%d", time.localtime())

	def get_jrrp(self) -> int:
		rplist = []
		for i in range(0, 101):
			for j in range(int(f(i, mul=60, sigma=40))):
				rplist.append(i)
		random.seed(self.id + self.date)
		result = rplist[random.randint(0, len(rplist) - 1)]
		return result

	def print_jrrp(self) -> str:
		result = self.get_jrrp()
		if result == 0:
			result = "你今天的人品值是：0，不要给我差评啊。"
		elif 0 < result < 10:
			result = "你今天的人品值是：%d，嗯，没错，是百分制。" % result
		elif 10 <= result < 50:
			result = "你今天的人品值是：%d，哇呜。。。" % result
		elif result == 50:
			result = "你今天的人品值是：%d，五五开。。。" % result
		elif 50 < result < 60:
			result = "你今天的人品值是：%d，还，，还行吧。。。" % result
		elif 60 <= result < 70:
			result = "你今天的人品值是：%d，是不错的一天呢！" % result
		elif 70 <= result < 80:
			result = "你今天的人品值是：%d，一般般啦！" % result
		elif 80 <= result < 90:
			result = "你今天的人品值是：%d，很不错的一天呢！" % result
		elif 90 <= result < 100:
			result = "你今天的人品值是：%d，好评如潮！！！" % result
		elif result == 100:
			result = "你今天的人品值是：%d，100! 100!! 100!!!" % result
		return result


if __name__ == '__main__':
	qq = '3232'
	jrrp = Jrrp(qq)
	print(jrrp.print_jrrp())
