from newscrawler.sentiment.mongo_tool import MongoTool
from newscrawler.sentiment.processString import CharLevel_preProcess

import newscrawler.sentiment.FileIO as FIO


class MySentences(object):
    def __init__(self, whichType='csv',collection='news',skip=4000, limit=2000,
                 filepath=None,filename=None,encoding='gbk'):
        self.filepath = filepath
        self.filename = filename
        self.whichType = whichType
        self.encoding= encoding
        self.collection= collection
        self.skip = skip
        self.limit = limit
    def __iter__(self):
        # try:
        #     with MongoTool() as mon:
        #         mongoGen1 = mon.MongoReadAll(collection='news')
        #         for data in mongoGen1:
        #             # 文本预处理
        #             content = CharLevel_preProcess(data)
        #             if content:
        #                 charList = self.stringToList(content)
        #                 yield charList
        # except Exception as e:
        #     print(e)
        #     pass
        # try:
        #     with MongoTool() as mon:
        #         mongoGen2 = mon.MongoReadAll(collection='comment')
        #         for data in mongoGen2:
        #             # 文本预处理
        #             content = CharLevel_preProcess(data)
        #             if content:
        #                 charList = self.stringToList(content)
        #                 yield charList
        # except Exception as e:
        #     print(e)
        #     pass
        try:
            for rows in FIO.load_News_csv(parentpath=self.filepath,
                                          filename=self.filename,
                                          encoding=self.encoding):
                for col in rows:
                    data = col[0]
                    # 文本预处理
                    content = CharLevel_preProcess(data)
                    if content:
                        charList = self.stringToList(content)
                        yield charList
        except Exception as e:
            print(e)
            pass

    @classmethod
    def csvToCharGen(self, parentpath ,filename ,encoding ):
        for rows in FIO.load_News_csv(parentpath=parentpath, filename=filename,
                                      encoding=encoding):
            for col in rows:
                data = col[0]
                # 文本预处理
                content = CharLevel_preProcess(data)
                if content:
                    charList = self.stringToList(content)
                    yield charList

    @classmethod
    def DBlimitToCharGen(self,collection, skip=4000, limit=2000):
        try:
            with MongoTool() as mon:
                mongoGen = mon.MongoReadLimit(collection=collection, skip=skip, limit=limit)
                for data in mongoGen:
                    # 文本预处理
                    content = CharLevel_preProcess(data)
                    if content:
                        charList = self.stringToList(content)
                        yield charList
        except Exception as e:
            print(e)
            pass

    @classmethod
    def DBAllToCharGen(self,collection):
        try:
            with MongoTool() as mon:
                mongoGen1 = mon.MongoReadAll(collection=collection)
                for data in mongoGen1:
                    # 文本预处理
                    content = CharLevel_preProcess(data)
                    if content:
                        charList = self.stringToList(content)
                        yield charList
        except Exception as e:
            print(e)

    @staticmethod
    def stringToList(content):
        charListBlank = " ".join(content)
        charList = charListBlank.split(' ')
        return charList