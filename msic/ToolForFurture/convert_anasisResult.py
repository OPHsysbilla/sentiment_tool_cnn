import  os

from newscrawler.sentiment.processString import rawContentPolish
def getAnalysisResult():
    source_dir = "D:\\hotpoint\\analysis_result"
    num = 0
    listDate = os.listdir(source_dir)
    res10000 = []
    for date in listDate:
        listClass = os.listdir(source_dir + "\\" + date)
        urlDic = {}
        urlFile = open(source_dir + "\\" + date + "\\" + "url.link", "r", encoding="utf-8")
        line = urlFile.readline().strip()
        while line:
            urlDic[line.split(" ")[0]] = line.split(" ")[1].strip()
            line = urlFile.readline()
        for clasNum in listClass:
            if os.path.isdir(source_dir + "\\" + date + "\\" + clasNum):
                newsList = os.listdir(source_dir + "\\" + date + "\\" + clasNum)
                for newsName in newsList:
                    if num > 211100:
                        try:
                            newFile = open(source_dir + "\\" + date + "\\" + clasNum + "\\" + newsName, "r", encoding="utf-8")
                            title = newsName.split(".")[0]
                            url = urlDic[newsName.split(".")[0]]
                            newFile.readline()
                            newFile.readline()
                            temp = []
                            tLine = newFile.readline().strip()
                            while tLine:
                                temp.append(tLine)
                                tLine = newFile.readline().strip()
                            content = "".join(temp)
                            content = rawContentPolish(content)
                            source = "搜狗新闻"
                        except Exception as e:
                            print("getAnalysisResult",e)
                        else:
                            res10000.append([title, content, date, source, url])
                            if num % 100 == 0:
                                print(num,"res1000-len:",len(res10000))
                                if res10000:
                                    yield  res10000
                                res10000 = []
                    num += 1
    if num % 100 != 0 :  #最后不足一万条的
        yield res10000
if __name__=="__main__":
    from newscrawler.utils.mysql_tool import MysqlTool
    mysql = MysqlTool()
    for lis in getAnalysisResult():
        mysql.insertManyNews(paramList=lis)

