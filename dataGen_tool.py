# coding:utf-8

import newscrawler.sentiment.config as cfg
from newscrawler.sentiment.JieBa_tool import delStopWord
from newscrawler.sentiment.processString import strPreProcess, CharLevel_preProcess

from newscrawler.sentiment.FileIO import loadAllTxtFromDir, load_News_csv

""" [注意文本 encoding]
    给出文件夹地址txtDirpath，返回每篇文章的分词seg_list 
"""
def txtDirToSegList(txtDirpath,encoding):
    for content in loadAllTxtFromDir(txtDirpath=txtDirpath,encoding=encoding):
        # 如果内容不为空
        if content:
            article = strPreProcess(content,returnType="string")
            seg_list = delStopWord(article)
            yield " ".join(seg_list)

""" 给出.csv数据集文件，返回每篇文章的分词seg_list """
def csvToSentences(parentpath,filename):
    for rows in load_News_csv(parentpath, filename):
        for row in rows:
            content = "".join(row)
            if content:
            # 新闻原文
                article = strPreProcess(content,returnType="string")
                seg_list = delStopWord(article)
                yield " ".join(seg_list)


""" 将csv 两栏文件 返回  labelX,maxSegLen """
def csvToLabelAndDataMaxLen(parentpath, filename,encoding,returnType="string"):
    labelX = []
    dataX = []
    maxSegLen = 0
    for rows in load_News_csv(parentpath=parentpath, filename=filename,encoding=encoding):
        for row in rows:
            label = row[0]
            data = row[1]
            # # 转换词向量
            # strpre = strPreProcess(data)
            # # strpre = 中国 土豪 瑞士买酒 一杯威士忌近元当地时间 瑞士圣莫里兹 当地的一家豪华酒店 维尔德豪斯酒店内展出的一杯的麦
            # seg_list = delStopWord(strpre)
            # # seg_list = ['中国', '土豪', '瑞士', '买酒', '一杯', '威士忌', '近元', '时间', '瑞士', '圣', '莫里兹']
            # maxSegLen = len(seg_list) if len(seg_list)> maxSegLen else maxSegLen
            # # maxSegLen = 2541
            # # content = " ".join(seg_list)

            # dataX.append(content)
            # from keras.preprocessing.text import one_hot,hashing_trick
            # hashing_trick(
            #               content,
            #               n=maxSegLen,
            #               hash_function='md5',
            #               filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
            #               lower=True,
            #               split=" "
            #               )
            maxSegLen = len(row) if len(row) > maxSegLen else maxSegLen
            labelX.append(label)
        return labelX,maxSegLen

""" 将csv 两栏文件 只返回List: labelX  """
""" 与csvToTexts一起使用 """
def csvToLabelList(parentpath, filename,encoding,returnType="string"):
    for rows in load_News_csv(parentpath=parentpath, filename=filename,encoding=encoding):
        labelX = []
        for row in rows:
            label = row[0]
            labelX.append(label)
        return labelX

""" 将csv 两栏文件 [只返回生成器data](String) 
    返回的是空格分开的“字”级句子
    与csvToTexts一起使用 
    可能为空
"""
def csvToTextGen(parentpath, filename,encoding,returnType="string"):
    for rows in load_News_csv(parentpath=parentpath, filename=filename,encoding=encoding):
        maxSegLen = 0
        for row in rows:
            data = row[1]
            # 文本预处理
            content = CharLevel_preProcess(data)
            if content:
                yield " ".join(content)
            else:
                yield ''

""" 读取MongoDB [只返回生成器data](String) 
    返回的是空格分开的“字”级句子
    与csvToTexts一起使用 
    可能为空
"""
def DBToTextGen(collection, skip=4000,limit=2000):
    from newscrawler.sentiment.mongo_tool import MongoTool
    with MongoTool() as mon:
        mongoGen = mon.MongoReadLimit(collection=collection,skip=skip,limit=limit)
        for data in mongoGen:
            # 文本预处理
            content = CharLevel_preProcess(data)
            if content:
                yield " ".join(content)
            else:
                yield ''



if __name__ == "__main__":
    # setting.py中目录路径
    extracted_path = cfg.extracted_news_dir
    reduced_path = cfg.Reduced_news_dir

    for labelX, maxSegLen in csvToLabelAndDataMaxLen(parentpath=cfg.allNews_csv_dir,
                                                       filename="comment1.csv", encoding='gbk'):
            print(labelX)
            print(maxSegLen)


    # # [注意文本 encoding]
    # # 给出文件夹地址txtDirpath，返回每篇文章的分词seg_list
    # from keras.preprocessing.text import one_hot
    # for s in txtDirToSegList(txtDirpath=reduced_path, encoding='GBK'):
    #     print(one_hot(s,
    #                   n=16000,
    #                   filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
    #                   lower=True,
    #                   split=" "
    #                   ))

    # # # 给出.csv数据集文件，返回每篇文章
    # from keras.preprocessing.text import one_hot
    # for s in csvToSentences(parentpath=cfg.Reduced_news_dir,
    #                            filename="Reduced.csv"):
    #     print(one_hot(s,
    #                   n=16000,
    #                   filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
    #                   lower=True,
    #                   split=" "
    #                   ))


    # allTextSplit  = []
    # for s in txtDirToSegList(txtDirpath=reduced_path, encoding='GBK'):
    #     allTextSplit.append(s)
    # allTextSplitWithBlack = " ".join(allTextSplit)
    # from sentiment.keras_tool import kerasPreProess,replaceEmbbading
    # print(allTextSplitWithBlack)
    # word_index, labels, x_train, y_train, x_test, y_test, x_val, y_val=\
    #     kerasPreProess(allTextSplitWithBlack)
    # replaceEmbbading(word_index, labels, x_train, y_train, x_test, y_test, x_val, y_val)



    # # 重定向
    # import sys
    # saveout = sys.stdout
    # with open('noNum.txt','w') as f:
    #     sys.stdout = f
    # sys.stdout = saveout
