from sys import argv
import requests
import datetime
import pprint

class AI:
    def __init__(self, category, paperNum, *item):
        self.category = str(category)
        self.paperNum = int(paperNum)
        # if args.__len__>0:
        if len(item)==1:
            self.item = str(item[0])

    def print_AI(self) -> str:
        url_base = "https://arxivapi.xixiaoyao.cn/paper/list/1?"
        date = "date="+str(datetime.date.today())
        category = "&category="+self.category
        data = requests.get(url=url_base+date+category)
        json = data.json()['result']
        result = ""
        if hasattr(self, 'item')==False:
            for i in range(self.paperNum):
                result = result + '『' + json[i]['title'] + '』\n'
        else:
            result = result + '『' + json[self.paperNum]['title'] + '』\n'
            result = result + json[self.paperNum][self.item]
        return(result)  

    def getAIHelp():
        return "category: NLP,CV,ML,IR,KG\npaperNum: recommend 1~5\nitem: abstract, paperurl, tags (if you enable this parameter, param1 will just be a serial number)"


if __name__ == '__main__':
    AI = AI("NLP", 5)
    print(AI.print_AI())
    

