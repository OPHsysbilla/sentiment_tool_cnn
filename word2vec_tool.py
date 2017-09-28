"""
功能：利用大语料生成词语的索引字典、词向量，然后保存为pkl文件
时间：2017年3月8日 13:19:40
"""

import pickle

MAX_SEQUENCE_LENGTH = 140  # 每条新闻最大长度
EMBEDDING_DIM = 128

import numpy as np

from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
import  newscrawler.sentiment.config as cfg
import  newscrawler.sentiment.ItelText as It
# 创建词语字典，并返回word2vec模型中词语的索引，词向量
def create_dictionaries(p_model):
    gensim_dict = Dictionary()
    gensim_dict.doc2bow(p_model.vocab.keys(), allow_update=True)
    w2indx = {v: k + 1 for k, v in gensim_dict.items()}  # 词语的索引，从1开始编号
    w2vec = {word:p_model[word] for word in w2indx.keys()}  # 词语的词向量
    return w2indx, w2vec

def gensimWord2VecModel(sentences,modelname):
    # sentences  获取句子列表，每个句子又是词汇的列表

    #  训练Word2vec模型（可尝试修改参数）
    model = Word2Vec(sentences,
                     size=EMBEDDING_DIM,  # 词向量维度
                     min_count=5,  # 词频阈值
                     window=5)  # 窗口大小

    #   保存的模型文件名
    saveModel(model, modelname=modelname)

    # model.save( cfg.word2vec_dir+ '\word2vec_update_comment.model') # 保存模型

def trainEmptyModel(modelname,some_sentences,more_sentences=None):
    model = Word2Vec(iter=1,min_count=4)  # an empty model, no training yet
    model.build_vocab(some_sentences)  # can be a non-repeatable, 1-pass generator
    if more_sentences:
        model = trainMore(model,more_sentences=more_sentences) # can be a non-repeatable, 1-pass generator
    saveModel(model=model,modelname=modelname)

def trainMore(model,more_sentences):
    print(model.corpus_count,model.iter)
    model.train(more_sentences,total_examples=model.corpus_count,epochs=model.iter)  # can be a non-repeatable, 1-pass generator
    return model

def saveModel(model,modelname ):
    model.save(cfg.word2vec_dir +'\\'+ modelname )  # 保存模型

def loadWord2VecModel(modelname='word2vec.model'):
    # gensim.models.KeyedVectors.load_word2vec_format(VECTOR_DIR, binary=True)
    model = Word2Vec.load( cfg.word2vec_dir+'\\'+modelname )
    return model


def savePkl():
    # 索引字典、词向量字典
    index_dict, word_vectors= create_dictionaries(model)

    # 存储为pkl文件
    pkl_name = raw_input(u"请输入保存的pkl文件名...\n").decode("utf-8")
    output = open(pkl_name + u".pkl", 'wb')
    pickle.dump(index_dict, output)  # 索引字典
    pickle.dump(word_vectors, output)  # 词向量字典
    output.close()

def getWordVecs(wordList):
    vecs = []
    for word in wordList:
        word = word.replace('\n', '')
        try:
            # only use the first 500 dimensions as input dimension
            vecs.append(model[word])
        except KeyError:
            continue
    # vecs = np.concatenate(vecs)
    return np.array(vecs, dtype = 'float')



if __name__ == "__main__":
    sentences = It.MySentences(whichType='csv',encoding='gbk',
                            filepath=cfg.allNews_csv_dir, filename="text.csv")

    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # gensimWord2VecModel(sentences,modelname='word2vec_update_comment.model')
    newsGen = sentences.DBAllToCharGen(collection='news')
    commentGen = sentences.DBAllToCharGen(collection='com')
    model = trainEmptyModel(modelname='word2vec_train_empty.model',some_sentences=newsGen
                            ,more_sentences=commentGen)
    # model = loadWord2VecModel('word2vec_train_empty.model')
    print(len(model.wv.vocab))
    # print(model.wv.vocab[''])
    for word in model.wv.vocab:
        print(word)
    # print(model.similarity('黔', '侗'))


