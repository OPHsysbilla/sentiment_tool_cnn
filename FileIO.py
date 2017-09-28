# coding:utf-8

import codecs
import collections
import csv
import os
import os.path

import newscrawler.sentiment.config as cfg

import newscrawler.sentiment.OSPath as oP


# 将重复10行的文本 extracted_news 以 标题内容 的形式 写入 csv 文件
def writeCsv_delTopN(path, BanList=None):
    with codecs.open(os.path.join(cfg.stopWords_parent_dir,"res.csv"), 'w', 'utf_8_sig') as csvFile3:
        writer2 = csv.writer(csvFile3,dialect='excel')
        writer2.writerow([u'标题',u'内容'])
        for filepath in getFile(path):
            #        -----             剔除前9行
            content = old_load_one_txt(filepath, 9)
            if BanList:
                #  如果内容不为空
                if content:
                    # 剔除 标题在BanList中的广告
                    title = content[0]
                    if not title in BanList:
                        writer2.writerow(content)
            else:
                if content:
                        writer2.wlriterow(content)


def csvOneToTwoCol(parentpath, filename):
    for rows in load_News_csv(parentpath, filename):
        for row in rows:
            # [禽兽，要么死刑、要么化学阉割。不然只坐牢放出来一样祸害人间']
            # ['1', '禽兽，要么死刑、要么化学阉割。不然只坐牢放出来一样祸害人间']
            newrow = [1,row]
            yield newrow


"""    将txtDirpath下所有txt文件，以单列[内容]的形式，写入 csv 文件  """
def writeCsv_FullContent(csvSavepath,csvSavename,txtDirpath):

    if not str(csvSavename).endswith(".csv"):
        raise NotImplementedError("In writeCsv_FullContent: write CSV file with no suffix '.csv',"
                             "please rename your 'savename' parameter.")

    csvFileSavepath = oP.join(csvSavepath, csvSavename)

    with codecs.open(csvFileSavepath, 'w', 'utf_8_sig') as csvFile:
        csvWriter = csv.writer(csvFile, dialect='excel')
        for content in loadAllTxtFromDir(txtDirpath=txtDirpath,encoding='GBK'):
            # 如果内容不为空
            if content:
                # afterPreProcess=strPreProcess(content,returnType="string")
                # if afterPreProcess and afterPreProcess.strip() != '':
                #     按行写入csv文件
                #     news = [afterPreProcess]
                csvWriter.writerow([1,content])
                csvFile.flush()

"""
os.path.walk()与os.walk()产生的文件名列表不同：
os.walk() 只产生文件路径
os.path.walk()    产生目录树下的目录路径和文件路径
"""
# 方法1：递归遍历目录
def visitDir1(path):
    li = os.listdir(path)
    for p in li:
        pathname = os.path.join(path, p)
        if not os.path.isfile(pathname):  # 判断路径是否为文件，如果不是继续遍历
            visitDir1(pathname)
        else:
            print(pathname)

# 方法3： 函数递归os.walk()
def getFile(dirpath,frontNum = 0):
    for root, dirs, files in os.walk(dirpath):
        for fileName in files:
            yield(os.path.join(root, fileName))


""" 读取文件夹txtDirpath下所有txt文件      """
def loadAllTxtFromDir(txtDirpath,encoding):
    for filepath in getFile(txtDirpath):
        content = []
        if encoding.find('GB')!=-1 or str(encoding).upper() == 'GBK':
            content = loadGBKTxt(filepath=filepath)
        elif str(encoding).lower()=='utf-8':
            content = loadFileWithEncoding(filepath=filepath,encoding='utf-8')
        else:
            content = loadFileWithEncoding(filepath=filepath, encoding=encoding)
        yield "".join(content)



def writelines_file(filepath,lines):
    with open(filepath, 'w') as f:
        #  跳过头部delTopLinesNum行
        f.writelines(lines)
"""
def writev_dict_csv(storePath,writeDict):
    # 从字典写入csv文件，没用到
    with open(storePath,'w', newline='') as csvFile3:
        writer2 = csv.writer(csvFile3)
        for key in writeDict:
            writer2.writerow([key, writeDict[key]])
"""
# \u3000 全角空格
def old_load_one_txt(filepath,delTopLinesNum=0):
    with open(filepath, 'r',encoding='utf-8') as f:
        #  跳过头部delTopLinesNum行
        lines = f.readlines()
        content = []
        for line in lines:  #  确定中文范围 : [\u4e00-\u9fa5]，范围内可能有表情符
            print(line)
            content.append(line.strip()
                           .replace("\u3000"," ")    # 全角空格
                           .replace("\ue40c"," "))   # 表情符
        yield content[delTopLinesNum:]
        # 返回字典 {"content": ,"title":  }

""" 读取文本，去除重复N行的文本 """
def loadTopNLineFromTxt(filepath,delTopLinesNum=0):
    with open(filepath, 'r',encoding='utf-8') as f:
        #  跳过头部delTopLinesNum行
        lines = f.readlines()
        content = []
        for line in lines:  #  确定中文范围 : [\u4e00-\u9fa5]，范围内可能有表情符
            raw = line.strip().replace("\u3000"," ").replace("\ue40c"," ")
            if delTopLinesNum:
                delTopLinesNum -= 1
                continue
            if raw:
                content.append(raw)   # 全角空格表情符
        yield content
        # 返回字典 {"content": ,"title":  }

""" 将重复10行的文本 extracted_news 
    以 [标题][内容] 的形式 写入 csv 文件 
"""
def write_News_csv(path,BanList=None):
    with codecs.open(os.path.join(path,"res.csv"), 'w', 'utf_8_sig') as csvFile3:
        writer2 = csv.writer(csvFile3,dialect='excel')
        writer2.writerow([u'标题',u'内容'])
        for filepath in getFile(path):
            #        -----             剔除前9行
            content = loadTopNLineFromTxt(filepath, 9)
            if BanList:
                #  如果内容不为空
                if content:
                    # 剔除 标题在BanList中的广告
                    title = content[0]
                    if not title in BanList:
                        writer2.writerow(content)
            else:
                if content:
                        writer2.wlriterow(content)

def write_csv(parentpath,savename,encoding,generator):
    if not os.path.exists(parentpath):
        os.mkdir(parentpath)
    with codecs.open(os.path.join(parentpath,savename), 'w', encoding=encoding) as csvFile3:
        writer2 = csv.writer(csvFile3,dialect='excel')
        for row in generator:
            writer2.writerow(row)

#    有utf_8_sig   utf-8  和 gbk三种格式
def check_csv(parentpath,filename,encoding='utf_8_sig'):
    with codecs.open(os.path.join(parentpath,filename), 'r',encoding=encoding ) as csvFile3:
        read = csv.reader(csvFile3,dialect='excel')
        ct = 0
        for rows in read:
            print('saved',rows)
            ct+=1
        print('共%s条' % ct)


def loadFile(parentpath, filename):
    if str(filename).endswith(".csv"):
        raise NotImplementedError(
            "FileIO.loadFile: please use loadCSV() to load '.csv' file, or you will encounter with encoding problem")
    filepath = oP.pathJoin(parentpath,filename)
    with open(filepath, 'r',encoding='utf-8') as f:
        lines = f.readlines()
        content = []
        for line in lines:
            content.append(line.strip())
        return content

def loadGBKTxt(filepath):
    if str(filepath).endswith(".csv"):
        raise NotImplementedError(
            "FileIO.loadFile: please use loadCSV() to load '.csv' file, or you will encounter with encoding problem")
    with open(filepath, 'r',encoding='gb18030',errors='ignore') as f:
        lines = f.readlines()
        linelist = []
        for line in lines:
            linelist.append(line.strip().replace('\u3000',''))
        return linelist

def loadFileWithEncoding(filepath,encoding):
    if str(filepath).endswith(".csv"):
        raise NotImplementedError(
            "FileIO.loadFile: please use loadCSV() to load '.csv' file, or you will encounter with encoding problem")
    with open(filepath, 'r',encoding=encoding) as f:
        lines = f.readlines()
        linelist = []
        for line in lines:
            linelist.append(line.strip().replace('\u3000',''))
        return linelist

def loadBinaryTxt(filepath):
    if str(filepath).endswith(".csv"):
        raise NotImplementedError(
            "FileIO.loadFile: please use loadCSV() to load '.csv' file, or you will encounter with encoding problem")
    with codecs.open(filepath, 'rb') as f:
        # print(chardet.detect(f.read())) #  rb读时检测
        return f.read()




def saveFile(parentpath, filename,data):
    if str(filename).endswith(".csv"):
        raise NotImplementedError(
            "FileIO.saveFile: please use saveCSV() to save '.csv' file, or you will encounter with encoding problem")
    filepath = oP.pathJoin(parentpath,filename)

    with open(filepath, 'w',encoding='utf-8') as f:
        if isinstance(data,str):
            f.write(data)
            f.flush()
        elif isinstance(data,collections.Iterable):
            f.writelines(data)
            f.flush()
        print("saveFile sucess:",filepath)


def loadCSV(parentpath, filename,encoding = 'utf_8_sig' ):
    with codecs.open(oP.pathJoin(parentpath, filename), mode='r',encoding=encoding) as csvFile:
        read = csvFile.reader(dialect='excel')
        return read

def loadUTFBOMTxt(parentpath, filename):
    with codecs.open(oP.pathJoin(parentpath, filename), 'r', 'utf_8_sig') as f:
        return f.read().split()


def load_News_csv(parentpath, filename,encoding='utf_8_sig'):
    with codecs.open(oP.pathJoin(parentpath, filename), 'r', encoding=encoding) as csvFile:
        read = csv.reader(csvFile,dialect='excel')
        yield read

def loadSomeSentences():
    for c in load_News_csv("D:\My\PyProject", "allNews.csv"):
        for title,article in c:
            print(title,article)

"""从文本中取出顶部的label"""
def splitLabelFromContent(parentpath, filename,encoding):
    for rows in load_News_csv(parentpath=parentpath
            , filename=filename, encoding='gbk'):
        for row in rows:
            # print(row)
            # ['1\t@京华时报【“我家狗累了，必须坐着！”】
            if row[0].find('\t') != -1:
                newrow = row[0].split('\t')
                yield newrow
            else:
                yield [1, row[0].strip()]


""" csv:将一行的['2\tcontent']utf-8格式转换为两行 [label,content]的GBK
     ['1\t@京华时报【“我家狗累了，必须坐着！”】]
"""
def covertCsvUtfToGBK(fromfilname,savename):
    # # CSV 内容  1行转两行带标签
    newrow = splitLabelFromContent(parentpath=cfg.allNews_csv_dir,
                                   filename=fromfilname,encoding='gbk')
    write_csv(parentpath=cfg.allNews_csv_dir,savename=savename,generator=newrow)
    check_csv(parentpath=cfg.allNews_csv_dir,filename=savename,encoding='gbk')

""" 整合多个csv文件变成一个 """
def loadManyCSVToOneRowGen(parentpath,filenameList,encoding='gbk'):
    for filename in filenameList:
        for rows in load_News_csv(parentpath=parentpath,filename=filename,encoding=encoding):
            for row in rows:
                yield row



if __name__ == "__main__":
    filenameList=['news2.csv',
                  'comment3.csv']
    TwoFileGen=loadManyCSVToOneRowGen(parentpath=cfg.allNews_csv_dir,
                                    filenameList=filenameList,
                                    encoding='gbk')

    write_csv(parentpath=cfg.allNews_csv_dir,savename='traindata2.csv',generator=TwoFileGen,encoding='gbk')
    check_csv(parentpath=cfg.allNews_csv_dir,filename='traindata2.csv',encoding='gbk')


    # covertCsvUtfToGBK(fromfilname='news1.csv',savename='news2.csv')



    # wrong_txt = r'D:\Project\files\Reduced\C000016\1063.txt'
    # a=loadGBKTxt(wrong_txt)
    # print(a)
    # utfText = r'D:\Project\files\extracted_news\extracted_news\1\1.txt'
    # b=loadFileWithEncoding(utfText,'utf-8')
    # print(b)


    # BanList = ['出租','出售','搜狐房产'] # 剔除 标题在BanList中的广告
    # writeCsv_delTopN(extracted_path,BanList=BanList)

    # # 读取dir下所有txt文件，写入.csv文件
    # writeCsv_FullContent(csvSavepath=cfg.allNews_csv_dir, csvSavename="Reduced.csv",
    #                  txtDirpath=cfg.Reduced_news_dir)







    # path = cfg.stopWords_parent_dir
    # s2700 = set(loadFile(path,'stopwords2700.txt'))
    # s1800 = set(loadFile(path,'stopwords1800.txt'))
    # s1500 = set(loadFile(path,'stopwords1500.txt'))
    # print(s1800-s1500)



