import numpy as np
import newscrawler.sentiment.config as cfg
from keras.models import load_model
from newscrawler.sentiment.dataGen_tool import csvToLabelAndDataMaxLen, csvToTextGen

from newscrawler.sentiment.FileIO import write_csv

MAX_SEQUENCE_LENGTH = 140  # 每条新闻最大长度
EMBEDDING_DIM = 128  # 词向量空间维度
VOCAB_SIZE = 999
VALIDATION_SPLIT = 0.05  # 验证集比例
TEST_SPLIT = 0.05  # 测试集比例
EPOCHES = 32
BATCH_SIZE = 64
LABEL_CLASS = 3  # 标签种类数  [1,0,-1]

""" 传入空格分词的句子 """
def textToSequences(word_index,inputList):
    sequences = []
    for string in inputList:
        from newscrawler.sentiment.processString import CharLevel_preProcess
        content = CharLevel_preProcess(string)
        char_list = content.split(' ')
        vect = []
        for w in char_list:
            i = word_index.get(w)
            if i is not None:
                vect.append(i)
        sequences.append(vect)
    return sequences

def TokenTestGen(parentpath,filename,encoding='gbk'):
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
    from keras.utils import to_categorical
    dataGen=csvToTextGen(parentpath=parentpath,
                               filename=filename,encoding=encoding)
    labelList,maxSegLen=csvToLabelAndDataMaxLen(parentpath=parentpath,
                               filename=filename,encoding=encoding)

    # tokenizer = Tokenizer(num_words=VOCAB_SIZE)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(dataGen)
    dataGenList=csvToTextGen(parentpath=parentpath,
                               filename=filename,encoding=encoding)
    sequences = tokenizer.texts_to_sequences(dataGenList)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    if modelname == 'mlp':
        data = tokenizer.sequences_to_matrix(sequences, mode='tfidf')
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    labels = to_categorical(labelList,num_classes=LABEL_CLASS)

    # print("data:",data)
    # print("labels:",labels)

    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)
    return maxSegLen,word_index,labels,data

import pickle
def writePklFile(modelname,filename):
    dir = cfg.pickle_dir+'\\'+modelname
    import  os.path
    if not os.path.exists(dir):
        os.mkdir(dir)
    filepath = dir + '\\'+filename
    output = open(filepath, 'wb')
    return output

def TokenTestWriteLabelAndData(modelname,labels,data):
    output = writePklFile(filename='label_data.pickle',modelname=modelname)
    # Pickle dictionary using protocol 0.
    pickle.dump(labels, output)
    pickle.dump(data, output)
    # Pickle the list using the highest protocol available.
    output.close()

def TokenTestWriteWordIndex(modelname,word_index):
    output = writePklFile(filename='word_index.pickle',modelname=modelname)
    pickle.dump(word_index, output)
    output.close()

def loadPklFile( modelname,filename):
    filepath = cfg.pickle_dir+'\\'+modelname+'\\'+filename
    pkl_file = open(filepath, 'rb')
    return pkl_file

def TokenTestLoadLabelAndData(modelname):
    pkl_file = loadPklFile(filename='label_data.pickle',modelname=modelname)
    labels = pickle.load(pkl_file)
    data = pickle.load(pkl_file)
    pkl_file.close()
    print("labels.shape",labels.shape)
    print("data.shape",data.shape)
    return  labels,data

def TokenTestLoadWordIndex(modelname):
    pkl_file = loadPklFile(filename='word_index.pickle',modelname=modelname)
    word_index = pickle.load(pkl_file)
    # {'说': 1, '中国': 2, '中': 3, '时间': 4, '美国': 5, '发生': 6, '里': 7
    pkl_file.close()
    print("word_index.shape",len(word_index))
    return word_index

def TokenTestTrain(word_index,labels,data,modelname):

    from keras.layers import Dense, LSTM, Dropout
    from keras.layers import Embedding,Activation,Conv1D,MaxPooling1D,Flatten
    from keras.models import Sequential

    p1 = int(len(data) * (1 - TEST_SPLIT))
    x_train = data[:p1]
    y_train = labels[:p1]
    x_test = data[p1:]
    y_test = labels[p1:]
    print('train docs: ' + str(len(x_train)),x_train.shape,y_train.shape)
    print('test docs: ' + str(len(x_test)),x_test.shape,y_test.shape)

    # 1 - lstm
    # model = Sequential()
    # model.add(Embedding(len(word_index) + 1, 128, input_length=MAX_SEQUENCE_LENGTH))
    # # model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))  # try using a GRU instead, for fun
    # # model.add(Dense(3,activation='sigmoid'))
    # model.add(Dropout(0.25))
    # model.add(Conv1D(filters=64,
    #                  kernel_size=3,
    #                  padding='valid',
    #                  activation='relu',
    #                  strides=1))

    # cnn - lstm
    # model.add(MaxPooling1D(pool_size=2))
    # model.add(LSTM(units=64,dropout=0.2,recurrent_dropout=0.2,return_sequences=True))
    # model.add(Conv1D(filters=32,
    #                  kernel_size=3,
    #                  padding='valid',
    #                  activation='relu',
    #                  strides=1))
    # model.add(MaxPooling1D(pool_size=2))
    # model.add(Dense(32,activation='sigmoid'))
    # model.summary()

    # # MLP
    # # 需要调整pad_sequence()为sequences to texts
    # model = Sequential()
    # model.add(Dense(512, input_shape=(len(word_index) + 1,), activation='relu'))
    # model.add(Dropout(0.2))
    # model.add(Dense(labels.shape[1], activation='softmax'))
    # model.summary()

    # # lstm - 3
    # model = Sequential()    #
    # model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
    # model.add(LSTM(32, return_sequences=True,dropout=0.2,
    #                recurrent_dropout=0.2,
    #                input_shape=(MAX_SEQUENCE_LENGTH, EMBEDDING_DIM)))  # returns a sequence of vectors of dimension 32
    # model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
    # model.add(LSTM(32))  # return a single vector of dimension 32
    # model.add(Dense(3, activation='softmax'))
    # model.summary()

    # model = Sequential()
    # model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM,  input_length=MAX_SEQUENCE_LENGTH))
    # model.add(LSTM(EMBEDDING_DIM, dropout=0.2, recurrent_dropout=0.2,return_sequences=True))
    # model.add(Conv1D(64, 3, padding='valid', activation='relu', strides=1))
    # model.add(MaxPooling1D(3))
    # model.add(Dropout(0.2))
    # model.add(Dense(43, activation='relu'))
    # model.add(Dropout(0.2))
    # model.add(Flatten())
    # model.add(Dense(3, activation='softmax'))
    # model.summary()

    # lstm - 1   14 epochs 80%
    # model = Sequential()
    # model.add(Embedding(input_dim=len(word_index)+1,output_dim=EMBEDDING_DIM,  input_length=MAX_SEQUENCE_LENGTH))
    # model.add(LSTM(EMBEDDING_DIM, dropout=0.2, recurrent_dropout=0.2,activation='relu'))
    # model.add(Dense(3))
    # model.add(Activation("softmax"))
    # model.summary()

    # # 第一个尝试的  0.32 0.32 0.32概率的模型 CNN
    model = Sequential()
    model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
    model.add(Dropout(0.2))
    model.add(Conv1D(250, 3, padding='valid', activation='relu', strides=1))
    model.add(MaxPooling1D(3))
    model.add(Flatten())
    model.add(Dense(EMBEDDING_DIM, activation='relu'))
    model.add(Dense(labels.shape[1], activation='softmax'))
    # plot_model(model, to_file='model.png',show_shapes=True)

    model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])
    saveModel(model=model,modelname=modelname)
    # 训练，交叉验证
    history = model.fit(x_train, y_train,
                        epochs=EPOCHES, batch_size=BATCH_SIZE)
    score = model.evaluate(x_test, y_test,
                           batch_size=BATCH_SIZE)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])

def saveModel(model,modelname):
    model.save(filepath=cfg.pickle_dir+'\\'+modelname+'\\'+'main.h5')

def loadModel(modelname):
    return load_model(filepath=cfg.pickle_dir+'\\'+modelname+'\\'+'main.h5')

def TokenTest(modelname,GenEmbedding=False):
    if GenEmbedding:
        TokenGenaEmbedding()
    TokenLoadAndTrain(modelname=modelname)

def TokenLoadAndTrain(modelname):
    word_index=TokenTestLoadWordIndex(modelname=modelname)
    labels, data = TokenTestLoadLabelAndData(modelname=modelname)

    TokenTestTrain(word_index=word_index,
                   labels=labels,
                   data=data,
                   modelname=modelname)

def TokenGenaEmbedding():
    maxSegLen,word_index,labels, data=TokenTestGen(parentpath=cfg.allNews_csv_dir,
                               filename="traindata2.csv",encoding='gbk')

    TokenTestWriteLabelAndData(modelname=modelname,labels=labels,data=data)
    TokenTestWriteWordIndex(modelname=modelname,word_index=word_index)


def updateEmotionMysql(table,id_name,modelname,forTest=False):
    ct = 0
    # 遍历 表 得到数据
    from newscrawler.sentiment.mysql_tool import MysqlTool
    mysql = MysqlTool()
    begin_cursor_id_without = ''
    while(True):
        last_cursor_id, docList = mysql.findNoneEmotionLimit(table=table,
                                                    begin_cursor_id_without=begin_cursor_id_without,
                                                    id_name=id_name,
                                                    limit=5000)
        # Todo 不同的表内容行不同 : news = title + content ; comment = content
        if table == 'news':
            inputList = [  " ".join([  doc.get('title') if doc.get('title') else '',
                                       doc.get('content') if doc.get('content') else ''
                                    ])  for doc in docList   ]
        elif table == 'comment':
            inputList = [  doc.get('content') for doc in docList if doc.get('content')    ]
        else:
            raise NotImplementedError("table should either be 'news' or 'comment', change inputList field if you want to get other table")
        # Todo 如果返回为空则不继续
        begin_cursor_id_without = last_cursor_id
        # loop is end, for no more data return from findLimit()
        if not inputList:
            break
        print(inputList)
        if forTest:
            print('测试模式 forTest：')
            emotionGen = TokenTestPredict(modelname=modelname, inputList=inputList,forTest=forTest)
            write_csv(parentpath=cfg.allNews_csv_dir+'\\emotion', savename='emotion-%s-%s.csv' % (modelname,ct),
                      generator=emotionGen, encoding='utf_8_sig')
            ct += 1
            if ct == 2:  # 5 个 5000已经够了
                return
        else:
            # Todo 对每一批输入序列进行预测，对每一批输出标签进行更新相应表
            paramList=[]
            for i,label in TokenTestPredict(modelname=modelname,inputList=inputList):
                # paramList  =  list of (table, emotion, id_name, id)
                paramList.append(( label, docList[i][id_name]))
            mysql.updatManyEmotion(table=table,
                                       id_name=id_name,
                                       paramList=paramList)

def insertEmotionMysql(modelname):
    from newscrawler.utils.mysql_tool import MysqlTool
    from newscrawler.msic.ToolForFurture.convert_anasisResult import getAnalysisResult
    mysql = MysqlTool()
    for lis in getAnalysisResult():
        if lis:
            inputList = [ " ".join([t[0],t[1]]) for t in lis  ]
            paramList = []
            for i, label in TokenTestPredict(modelname=modelname, inputList=inputList):
                # paramList  =  list of (table, emotion, id_name, id)
                lis[i].append(label)
                paramList.append(tuple(lis[i]))
            mysql.insertManyNews( paramList=paramList)



""" 模型构建好后预测 """
def TokenTestPredict(modelname,inputList,forTest=False):
    model = loadModel(modelname)
    from keras.preprocessing.sequence import pad_sequences
    word_index = TokenTestLoadWordIndex(modelname=modelname)
    sequences = textToSequences(word_index=word_index,inputList=inputList)
    XX = pad_sequences(sequences=sequences, maxlen=MAX_SEQUENCE_LENGTH)
    if modelname=='mlp':
        XX = pad_sequences(sequences=sequences, maxlen=len(word_index)+1)
    print('predictions.shape: ', XX.shape)

    predicts = model.predict(XX)
    predictList = np.ndarray.tolist(predicts)
    labels = [x.index(max(x)) for x in predictList]
    label2word = {2: '正向', 1: '中性', 0: '负向'}
    for i in range(len(inputList)):
        if forTest:
            print('predictions.res: ')
            print('负 中 正')
            # 测试用，输出到csv，返回生成器
            print(predicts[i],label2word[labels[i]],inputList[i])
            yield labels[i],inputList[i]
            # print('{}   {}'.format(label2word[labels[i]], inputList[i]))
            # labelList.append(label2word[labels[i]])
        else:
            yield i,label2word[labels[i]]

def labelEmotion():
    modelname = 'cnn'
    updateEmotionMysql(
        modelname=modelname,table='news',id_name='docId')
    updateEmotionMysql(
        modelname=modelname,table='comment',id_name='id')


if __name__ == "__main__":
    modelname = 'cnn'

    # 取出allNews
    insertEmotionMysql(modelname=modelname)

    # TokenTest(GenEmbedding=False,  # 每次换新model总是为true，是否根据数据生成词向量
    #           modelname=modelname)


    # # forText为True：测试输出到csv
    # # forText为False：修改所有mysql里的内容

    # updateEmotionMysql(
    #     forTest=False,
    #     modelname=modelname,table='news',id_name='docId')


