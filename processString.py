# encoding=utf-8

import codecs
import csv
import re

import newscrawler.sentiment.JieBa_tool as Jba
import newscrawler.sentiment.OSPath as oP
import newscrawler.sentiment.config as cfg

import newscrawler.sentiment.FileIO as FIO


# \u3000 全角空格




def cut_word_into_matrix(path,BanList=None):
    # 除去全角的所有新闻条目   .csv
    # parent_dir = oP.split(path)[0]  ==  allNews_csv_dir
    csvFile_path = oP.join(cfg.allNews_csv_dir, "allNews.csv")
    csvFile =codecs.open(csvFile_path, 'w', 'utf_8_sig')
    writer2 = csv.writer(csvFile, dialect='excel')
    writer2.writerow([u'标题', u'内容'])

    # 分词后的文件
    fseg_path = oP.join(cfg.allNews_csv_dir, "seg_list.txt")
    with open(fseg_path, 'w', encoding='utf-8') as fseg:
        for filepath in FIO.getFile(path):
            #        -----             剔除txt文件前9行的重复标题
            for content in FIO.loadTopNLineFromTxt(filepath, 9):
                #  如果内容不为空
                # 文字处理 去除全角
                try:
                    title =  FullToHalf(content[0])
                    artic = FullToHalf(content[1])
                    news = [title, artic]
                    writer2.writerow(news)
                    csvFile.flush()
                    # 剔除 标题在BanList中的广告
                    if BanList and not isAds(title):
                        total_content = " ".join(news)
                        dropPunc_content = dropPunctuation(total_content)
                        seg_list = Jba.JieBaWordDealt(dropPunc_content)  # 默认是精确模式
                        for seg in seg_list:
                            fseg.write(seg)
                            fseg.write('|')
                        # os.linesep 可以根据系统自动选择换行符
                    fseg.flush()
                except Exception as err:
                    print(err)
    csvFile.close()


def dropPuncExceptComma(s):
    # # 去除逗号句号分号，改用","断句
    # stopSym = r'[/，]'
    # dropStopSym = reSub(pattern=stopSym, repl='，', string=s)

    # # 去除符号(不匹配,)
    dropOtherSym = r'(?!,.)\W+'
    temp = reSub(pattern=dropOtherSym,repl = ' ',string=s)

    # 去除连续空格
    blank_space = r'\s+'
    res = reSub(pattern=blank_space,repl = ' ',string=temp)
    return res


""" 字符串去除符号，用','断句，没有其他符号 """
def dropPunctuation(s):
    # 去除符号(所有符号)
    dropOtherSym = r'\W+'
    temp = reSub(pattern=dropOtherSym,repl = ' ',string=s)

    # 去除连续空格
    blank_space = r'\s+'
    res = reSub(pattern=blank_space,repl = ' ',string=temp)

    return res

def dropBlankSpace(s):
    blank_space = r'\s+'
    res = reSub(pattern=blank_space,repl = '',string=s)
    return res


""" 封装的re.sub函数 """
def reSub(pattern,string,repl):
    comp = re.compile(pattern= pattern,
                     flags=re.U)
    res = comp.sub(repl=repl,string=string)
    return res


""" 断句 ： 根据空格 与 逗号句号问号感叹号等断句  
 
    剩下的句子仍然包括　时间、(责任编辑)、''、 
    * 责任编辑、作者等一般在列表最后两个，可以去掉  
　  ⊙ · /  :  、 等都是\W+可以分词的
    《》()[]【】 可以考虑断句， 但此处用作分词
"""
def reSplit(string):
    splitPattern = r"\s+|[,，。?!？！]"
    res = re.split(pattern=splitPattern,flags=re.U,string=string)
    return res[:-2]


""" 符号替换 英-中 或者 对应映射替换（不用） """
def replaceCnToEn(s):
    # cn_punctuation = r'！？“”#$&‘’（）*+-，。、：；《》=@……——·~{|}【】⊙'
    # en_punctuation = r'!?""#$&''()*+-,.,:;<>=@^_``{|}[]-'
    fromstr = r'！？‘’，、。“”（）【】'
    tostr = r'!?"",,,""()[]'
    transtab = s.maketrans(fromstr,tostr)
    return s.translate(transtab)

""" 判断是否是广告（未完善）  """
def isAds(title,BanList=None):
    #  如果内容不为空
    flagIsAds = False
    # 剔除 标题在BanList中的广告
    if title:
        if BanList:
            if title in BanList:
                flagIsAds = True
    return flagIsAds

# pattern = r"(\(\S+\))" # 去除括号内文字 例如 (图) (本报讯:)
# pattern = r"(((\d+\.)?\d+[\u4e00-\u9fa5]+)|)" #后面是中文的数字的
# pattern = "(?!\d+)[\u4e00-\u9fa5]+" #后面不是数字的中文
""" 去除所有数字只剩下数字后的符号　%  $ 等
    # 所有数字包括正负号
    # 包括数字后的一个中文 例如3000吨  1523.56元
    # 日期会被去掉只剩下符号   例如2007-05-06  2001/05/06
    # 去除括号内文字 例如 (图) (本报讯:)    

    #  before = '-1000 123.5  0.2% 2017年10月10日 3000吨  1523.56元起吧  12.123.45  2007-05-06  2001/05/06 (图) (本报讯:) (来源：中华网)'
    #  after  =  %    起吧  .    //   
"""
def NoNumbers(string):
    number = r"(((\d+\.)?\d+[\u4e00-\u9fa5]?)|([+-])?\d+(\.\d+%?)?)|(\<[^()]+\>)"  # 括号内的保留
    # number = r"(((\d+\.)?\d+[\u4e00-\u9fa5]?)|([+-])?\d+(\.\d+%?)?)|(\([^()]+\))"  # 括号内的不要，取掉所有数
    # number = r"(((\d+\W)?\d+(\W|[\u4e00-\u9fa5])?)|([+-])?\d+(\.\d+%?)?)|(\(\S+\))"  # 前面不是.的数字
    res = re.sub(pattern=number, flags=re.U,
                 string=string, repl='')
    return res


""" 预处理
    # 去除&nbsp，去除空格
"""
def NoNbsp(s):
    # return s.replace(old='&nbsp',new='')
    return reSub(pattern=r'(&nbsp)+',
                 repl='',
                 string=s)

""" 字符串全角转半角  """
def FullToHalf(ustring) :
    strList = []
    for ch in ustring:
        inside_code=ord(ch)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
            strList.append(chr(inside_code))
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248
            strList.append(chr(inside_code))
        else:
            strList.append(ch)
            continue
    return "".join(strList)


""" 读取allNews.csv　　断句的实例

    保留句子内符号，去掉了,，。?!？！
    
    返回句子的list
"""
def allNewsToSentences():
    for c in FIO.load_News_csv(cfg.allNews_csv_dir, "allNews.csv"):
        for title,article in c:
            content = "".join([title,article])
            # 新闻原文 raw content
            s = strPreProcess(content)
            yield s





""" 文本预处理  string  """
def strPreProcess(string,returnType="string"):
    # 处理半角
    # print('a:',string)
    # noSpace = dropBlankSpace(string)
    # 一开始不取掉空格，使得本身拥有的空格保存方便断句
    noHalf = FullToHalf(string)
    noNbsp = NoNbsp(noHalf)
    noSpace = dropBlankSpace(noNbsp)
    cnToEnSym = replaceCnToEn(noSpace)
    noNum = NoNumbers(cnToEnSym)
    # 不断句则取掉所有符号
    if returnType != "list":
        noPunc = dropPunctuation(noNum)
        # print('b:', noPunc)
        return noPunc
    # 断句则以逗号句号为分割，句内符号未消除
    else:
        s = reSplit(noNum)
        # print('c:', s)
        return s

def rawContentPolish(string):
    noHalf = FullToHalf(string)
    noNbsp = NoNbsp(noHalf)
    noSpace = dropBlankSpace(noNbsp)
    # cnToEnSym = replaceCnToEn(noSpace)
    # noPunc = dropPuncExceptComma(cnToEnSym)
    return noSpace

""" 按 字 分割
    所有文本需要处理的最高封装：
    将raw文本：预处理、去停用词、重新合并 
"""
def CharLevel_preProcess(string):
    # 文本预处理
    content = strPreProcess(string).replace('原标题', '').strip()
    return " ".join(content)
def WordLevel_preProcess(string):
    # 文本预处理
    strpre = strPreProcess(string).replace('原标题', '').strip()
    seg_list = Jba.delStopWord(strpre)    # strpre = 中国 土豪 瑞士买酒 一杯威士忌近元当地时间 瑞士圣莫里兹 当地的一家豪华酒店 维尔德豪斯酒店内展出的一杯的麦
    content = " ".join(seg_list)  # seg_list = ['中国', '土豪', '瑞士', '买酒', '一杯', '威士忌', '近元', '时间', '瑞士', '圣', '莫里兹']
    return content

if __name__ == "__main__":
    path = r"D:\My\PyProject\extracted_news"
    BanList = ['出租','出售','搜狐房产'] # 剔除 标题在BanList中的广告
    # 处理 extracted_news下所有新闻  变成 allNews.csv
    # cut_word_into_matrix(path,BanList=BanList)


    # # 读取 allNews.csv 处理
    # for c in FIO.load_News_csv(cfg.allNews_csv_dir, "allNews.csv"):
    #     for title,article in c:
    #         print(title,article)
    #         Jba.JieBaWordDealt(content)

