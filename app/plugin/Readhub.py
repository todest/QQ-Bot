import requests
import json


def getNews(number) -> str:
	number = number if number else '5'
	assert number.isdigit()
	assert int(number) in range(1, 21)
	api = "https://api.readhub.cn/topic?lastCursor=&pageSize=" + number
	req = requests.get(url=api)
	if req.status_code != 200:
		return "".join("HTTP GET ERROR!")
	news_digest = ""
	resp_json = json.loads(req.text)
	news_list = resp_json["data"]
	for news in news_list:
		cur_news = news["title"] + "\r\n\r\n"
		news_digest += cur_news
	return news_digest


if __name__ == '__main__':
	print(getNews('1'))
