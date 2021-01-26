import requests
import json as js
import random

def getNews(number:int = 5) -> str:
    api = "https://api.readhub.cn/topic?lastCursor=&pageSize=" + str(number)
    req = requests.get(url=api)
    # print("status_code: ", req.status_code)
    if req.status_code != 200:
        return "".join("HTTP GET ERROR!")

    newsDigest = ""

    json = js.loads(req.text)

    newsList = json["data"]

    for news in newsList:
        # print(news["title"])
        # print(news["summary"])
        curNews = news["title"] + "\r\n\r\n"
        newsDigest += curNews
    return newsDigest

if __name__ == '__main__':
    print(getNews())