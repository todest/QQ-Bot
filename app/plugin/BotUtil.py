def parseArgs(plain_str) -> list:
	args = plain_str.strip().split()
	for i in range(len(args)):
		args[i].strip()
	args.pop(0)
	return args


if __name__ == '__main__':
	res = parseArgs(".jrrp")
	if res:
		print(res)
