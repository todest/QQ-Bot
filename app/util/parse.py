from typing import List


# 拆分指令参数为一个列表，并去除入口指令
def parse_args(plain_str) -> list:
	args: List[str] = plain_str.strip().split()
	for i in range(len(args)):
		args[i].strip()
	args.pop(0)
	return args


if __name__ == '__main__':
	res = parse_args(".jrrp")
	if res:
		print(res)
