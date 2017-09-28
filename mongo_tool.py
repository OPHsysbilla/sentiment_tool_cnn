import pymongo

import newscrawler.sentiment.config as cfg

list_news= [
            {"$group": {
                "_id": {"docId": "$docId", "title": "$title", "createTime": "$createTime", "url": "$url",
                        "content": "$content",
                        "source": "$source"},
                "repeat": {"$sum": 1}}},
            {"$sort": {"repeat": -1}}
        ]
list_comment = [
    # {"$skip": 0},
    # {"$limit": 200},
    {"$group": {
        "_id": {"docId": "$docId", "location": "$location",
                "createTime": "$createTime", "nickname": "$nickname", "content": "$content",
                "vote": "$vote", "against": "$against"},
        "repeat": {"$sum": 1}}},

]
# for i in cs.distinct("content"):
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
# client.close()

list_C = [
    # {"$skip": 0},
    {"$limit": 2000}, {"$sort": {"vote": -1, "against": -1}}
]

# a = list(cs.aggregate(list_comment))


import codecs, csv
class MongoTool(object):
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['cocoke']
        self.news = self.db['news']
        self.comment = self.db['comment']
        self.setting = self.db['setting']
        self.dictSetting = {
            '_id': "cocoke",
        }
    def __del__(self):
        self.client.close()


    """数据库读limit个文档"""
    def MongoReadLimit(self,collection,skip=0,limit=2000):
        for doc in self.db[collection].find().skip(skip).limit(limit).sort(
                # [("vote", pymongo.DESCENDING), ("against", pymongo.DESCENDING)]):  # 使用distinct方法，获取每一个独特的元素列表
                [("createTime", pymongo.DESCENDING)]):  # 使用distinct方法，获取每一个独特的元素列表
            content = doc['content']
            yield content.strip()

    """数据库读所有Content"""
    def MongoReadAll(self,collection):
        for doc in self.db[collection].find({},no_cursor_timeout=True):
            content = doc['content']
            yield content.strip()

    """数据库读所有文档"""
    def MongoReadAllDoc(self,collection):
        for doc in self.db[collection].find({},no_cursor_timeout=True):
            yield doc


    """数据库读limit个文档"""
    """怪在保存utf_8_sig，修改了打开必须要不是utf的格式手动保存，没修过则utf_8_sig"""
    def MongoGenCsv(self,skip,limit,collection,filename):
        with codecs.open(cfg.allNews_csv_dir + "\\" +filename, 'w', 'utf_8_sig') as csvFile3:
            writer2 = csv.writer(csvFile3, dialect='excel')
            for doc in self.db[collection].find().skip(skip).limit(limit).sort(
                    # [("vote", pymongo.DESCENDING), ("against", pymongo.DESCENDING)]):  # 使用distinct方法，获取每一个独特的元素列表
                    [("createTime", pymongo.DESCENDING)]):  # 使用distinct方法，获取每一个独特的元素列表
                content = doc['content']
                writer2.writerow([1, content.strip()])

    def find_one(self,keyword):
        dicCom = {"_id": '0000000000000000'}
        print(self.news.find_one(dicCom))
        return self.news.find_one(dicCom)
if __name__=='__main__':
    mongoTool = MongoTool()
    mongoTool.find_one('_id')
    # mongoTool.MongoGenCsv(skip = 0,
    #                       limit=1000,
    #                       collection='news',
    #                       filename='news1.csv'
    # )
