SAVE_COMMENT_DIR = r'D:\MongoDB\savejson\comment'
SAVE_NEWS_DIR = SAVE_COMMENT_DIR


if __name__=='__main__':

    import pymongo
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['cocoke']
    news = db['news']
    nt = db['news_table']
    cs = db['comments']
    comment = db['comment']
    listParam = [

        {"$group": {"_id": {"docId":"$docId", "title":"$title", "createTime":"$createTime", "url":"$url","content":"$content","source":"$source"},
        "repeat": { "$sum": 1}}},
        {"$sort": {"repeat": -1}}
    ]
    list_comment = [
        # {"$skip": 0},
        # {"$limit": 200},
        {"$group": {
            "_id": {"docId": "$docId", "location": "$location",
                    "createTime": "$createTime", "nickname": "$nickname", "content": "$content",
                    "vote": "$vote","against": "$against"},
            "repeat": {"$sum": 1}}},

    ]
    setting = db['setting']
    dictSetting = {
        'crawlInterval':12,
        '_id': "cocoke",
        "keyWord":['新疆']
    }
    # setting.save(dictSetting)
    dicSet = setting.find_one({'crawlInterval': 12})
    crawlInterval = dicSet['crawlInterval']
    print('crawlInterval: ', crawlInterval, ' hours')



    #
    # ct=0
    # for i in cs.distinct("content"):
    #     ct+=1
    #     item = cs.find_one({'content': i})
    #     new=dict()
    #     new['docId']= item['docId']
    #     new['location']= item['location']
    #     new['createTime'] = item['createTime']
    #     new['nickname'] = item['nickname']
    #     new['content'] = item['content']
    #     new['vote'] = item['vote']
    #     new['against'] = item['against']
    #     comment.save(new)
    # print(ct)
    list_C = [
        # {"$skip": 0},
        {"$limit": 2000},{"$sort": {"vote":-1,"against":-1}}
    ]

    # a = list(cs.aggregate(list_comment))
    ct = 0
    import codecs,csv
    with codecs.open('text2.csv', 'w', 'utf_8_sig') as csvFile3:
        writer2 = csv.writer(csvFile3,dialect='excel')
        for doc in comment.find().skip(4000).limit(2000).sort([("vote",pymongo.DESCENDING),("against",pymongo.DESCENDING)]):  # 使用distinct方法，获取每一个独特的元素列表
            content = doc['content']
            writer2.writerow([1,content])


            # item = doc['_id']
            # new=dict()
            # new['_id']= item['docId']
            # new['location']= item['location']
            # new['createTime'] = item['createTime']
            # new['nickname'] = item['nickname']
            # new['content'] = item['content']
            # new['vote'] = item['vote']
            # new['against'] = item['against']
            # comment.save(new)
    client.close()

# tag = getattr(self, 'tag', None)
#     url = url + 'tag/' + tag

# def findTophref(self,response):
#     tabContents = response.css('.tabContents')
#     reFindAllHref(tabContents)
#
#     EndText = response.css('#endText').extract()
#     extractLabelP(EndText)
#
#     # 找docId
#
#
# def ShowAll(self,response,startUrls):
#     for url in startUrls:
#         fetch(url)
#
#         tabContents = response.css('.tabContents')
#         for x,y in reFindAllHref(tabContents):
#             whichType = howToExtractContent(x)
#             fetch(x)
#
#             NewsUrl = response.url
#             scrip_content = self.getScriptText(response)
#             docId = findKeyWordJson(html_content=scrip_content
#                                     , keyword='docId')
#             productKey = findKeyWordJson(html_content=scrip_content
#                                          , keyword='productKey')
#
#             if whichType == typeNews['news']:
#                 # 抽取内容
#                 EndText = response.css('#endText').extract()
#                 content = extractLabelP(EndText)
#                 # 抽取其他
#
#                 title = response.css('h1::text').extract_first()
#                 timee = response.css('.post_time_source::text').extract_first()
#                 source =  response.css('.post_time_source>a::text').extract_first()
#                 creatTime = extractTime(timee)
#                 dicN = makeNewsDict(url=NewsUrl,
#                                     docId=docId,
#                                     title=title,
#                                     createTime=creatTime,
#                                     content=content,
#                                     source=source)
#                 # 保存
#                 saveNews(dicN)
#
#             # 网易号 ,id = content
#             elif whichType== typeNews['dy']:
#                 EndText = response.css('#content').extract()
#                 content = extractLabelP(EndText)
#                 # 抽取其他
#                 title = response.css('h2::text').extract_first().strip()
#                 source = '网易号'
#                 creatTime = response.css('.time>span::text').extract_first()
#                 dicN = makeNewsDict(url=NewsUrl,
#                                     docId=docId,
#                                     title=title,
#                                     createTime=creatTime,
#                                     content=content,
#                                     source=source)
#                 # 保存
#                 saveNews(dicN)
#
#             # 图集，是读取textArea内的内容
#             # others可以不管正文，一般是直播之类的
#             elif whichType== typeNews['photoview'] or whichType==typeNews['others'] :
#                 # 尝试读取textArea
#                 textAreaLabel = response.css('textarea::text').extract()
#                 if textAreaLabel:
#                     # 提取textArea内文本
#                     nexturls,textAreaDic = extractTextArea(textAreaLabel)
#                     # 读取下一个链接
#                     for url in nexturls:
#                         yield Request(url=url, callback=self.parse_new)
#                     # 保存读取的信息
#                     textAreaDic['docId']=docId
#                     textAreaDic['url']=NewsUrl
#                     saveNews(textAreaDic)
#
#             # 分析评论Api的第一页
#             # 需要在script中查找docId
#             # 提取 "docId"
#
#             new_url = generateCommentApi(scrip_content=scrip_content,
#                                          offset=0,
#                                          docId=docId,
#                                          productKey=productKey,
#                                          ListType='newList')
#             yield Request(url=new_url, callback=self.parse_comment)
