import requests


def getHitokotoHelp():
	text = "a\t动画\r\nb\t漫画\r\nc\t游戏\r\nd\t文学\r\ne\t原创\r\nf\t来自网络\r\ng\t其他\r\nh\t影视\r\ni\t诗词\r\nj\t网易云\r\nk\t哲学\r\nl\t抖机灵"
	return text


def getHitokoto(str_type=None) -> str:
	api_url = 'https://v1.hitokoto.cn'
	data = {
		'encode': 'text',
		'charset': 'utf-8'
	}
	if str_type:
		assert str_type in [chr(i) for i in range(ord('a'), ord('m'))]
		data.update({'c': str_type})
	result = requests.get(api_url, params=data)
	result = result.content.decode('utf-8')
	return result


if __name__ == '__main__':
	print(getHitokoto('a'))
