from datetime import datetime

import pymysql.cursors

""" 注意返回字典中'time'字段: datetime.datetime(2017, 8, 29, 12, 37, 54) 
                'emotion'字段 :int
                其余均为字符串
"""


class MysqlTool(object):
    def __init__(self):
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'db': 'cocoke',
            'charset': 'utf8mb4',  #charset='utf8'
            'cursorclass': pymysql.cursors.DictCursor,
        }
        # Connect to the database
        self.conn = pymysql.connect(**config)
    def __del__(self):
        self.conn.close()


    def findNewsNoInTable(self):
        """有评论没新闻的新闻
        select docId,url from  news
        where commentNum is  null
        :return:
        """
        with self.conn.cursor() as cur:
            sql = "select docId,url from  news"+ \
                  "where commentNum is  null"
            try:
                cur.execute(sql)
                results = cur.fetchall()  # list of dicts
                self.conn.commit()
                docIdList = [dic['docId'] for dic in results]
                urlList = [dic['url'] for dic in results]
                return docIdList,urlList
            except Exception as e:
                print(e)
                self.conn.rollback()

    #  寻找没有标注感情emotion域的
    def findNoneEmotionLimit(self,table,id_name,begin_cursor_id_without='',limit=1000):
        with self.conn.cursor() as cur:
            # SELECT * FROM news where emotion is null and docId > ''  order by docId asc limit 5000
            sql = "SELECT * FROM %s WHERE emotion is null AND %s > '%s' " \
                  "ORDER BY %s ASC LIMIT %s" % (table,id_name,begin_cursor_id_without,id_name,limit)
            print (sql)
            try:
                # Execute the SQL command
                cur.execute(sql)
                # Fetch all the rows in a list of lists.
                results = cur.fetchall() #list of dicts
                # for next page , next call this function, where put last_cursor_id = begin_cursor_id
                last_cursor_id = results[-1][id_name] if results else ''
                self.conn.commit()
                return last_cursor_id,results
            except Exception as e:
                print(e)
                self.conn.rollback()

    def findLimit(self,table,id_name,begin_cursor_id_without='',limit=1000):
        with self.conn.cursor() as cur:
            # sql = "SELECT * FROM %s OFFSET %d LIMIT %d" % (table,offset,limit)
            sql = "SELECT * FROM %s WHERE %s > '%s' " \
                  "ORDER BY %s ASC LIMIT %s" % (table,id_name,begin_cursor_id_without,id_name,limit)
            print (sql)
            try:
                # Execute the SQL command
                cur.execute(sql)
                # Fetch all the rows in a list of lists.
                results = cur.fetchall() #list of dicts
                # for next page , next call this function, where put last_cursor_id = begin_cursor_id
                last_cursor_id = results[-1][id_name] if results else ''
                self.conn.commit()
                return last_cursor_id,results
            except Exception as e:
                print(e)
                self.conn.rollback()

    def updatManyEmotion(self,table,id_name,paramList):
        """ paramList = (table,emotion,id_name,id) """
        with self.conn.cursor() as cur:
            sql = "UPDATE "+ table +" SET emotion = %s WHERE "+ id_name +" = %s"
            try:
                cur.executemany(sql,paramList)
                self.conn.commit()
            except Exception as e:
                print('updatManyEmotion:',e)
                self.conn.rollback()

    def insertOneDic(self,dic):
        # 执行sql语句
        try:
            columnList=dic.keys()

            valueList=dic.values()
            columns = ",".join(columnList)
            values = ",".join(valueList)

            with self.conn.cursor() as cursor:
                # 执行sql语句，进行查询
                sql = 'INSERT INTO mycom ('+ columns +')' \
                      ' VALUES('+ values +')'
                # print('插入',sql)
                cursor.execute(sql)
                self.conn.commit()
                # 获取查询结果
                result = cursor.fetchone()
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        except Exception as e:
            print(e)
            self.conn.rollback()


            ##插入
    def convertDocToNewsItem(self,doc):
        news = {}
        from newscrawler.sentiment.processString import rawContentPolish
        value = rawContentPolish(doc['content'])
        for key in doc:
            if key == '_id':
                news['docId'] = "'" + str(doc[key]) + "'"
            elif key == 'content':
                news[key] = "'" + str(value) + "'"
            else:
                news[key]="'"+str(doc[key])+"'"
        # news['createTime'] = datetime.strptime(doc['createTime'], "%Y-%m-%d %H:%M:%S")
        # print(type(news['createTime']))
        return news

    def convertDocToComment(self,doc):
        news = {}
        from newscrawler.sentiment.processString import rawContentPolish
        # value = rawContentPolish(doc['content'])
        for key in doc:
            if key == '_id':
                news['id'] = "UUID()"
            elif key == 'content':
                news[key] = "'"+rawContentPolish(str(doc[key]))+"'"
            else:
                news[key]="'"+str(doc[key])+"'"
        # news['createTime'] = datetime.strptime(doc['createTime'], "%Y-%m-%d %H:%M:%S")
        # print(type(news['createTime']))
        return news

""" 
更新 评论数 
update news,(
select count(*) as ct,docId from comment
where comment.docId in (select news.docId from news)
group by comment.docId
) as tempT
set news.commentNum = tempT.ct where news.docId = tempT.docId;


有评论没新闻
select count(*) as ct,docId from comment
            where comment.docId not in (select news.docId from news)
            group by  docId
         
有新闻没评论            
select * from news  where news.docId not in (select docId from comment)            
SELECT  *  FROM `news` where commentNum is null

评论数量太少（小于15条）的新闻
select count(*) as ct,docId from comment 
group by docId
having ct < 15
ORDER BY ct desc


"""




""" 不是成员函数 
    遍历整个表：优化的方法（样例）
"""
def WalkThroughTableSample():
    mysql = MysqlTool()
    begin_cursor_id_without = ''
    while (True):
        last_cursor_id, inputList = mysql.findLimit(table='comment',
                                                    begin_cursor_id_without=begin_cursor_id_without,
                                                    id_name='id',
                                                    limit=10000)
        print(len(inputList))
        begin_cursor_id_without = last_cursor_id
        # loop is end, for no more data return from findLimit()
        if not inputList:
            break

if __name__=='__main__':
    # res = time.strptime('2017-08-22 17:39:54', "%Y-%m-%d %H:%M:%S")  # <class 'time.struct_time'>
    res = datetime.strptime('2017-08-22 17:39:54', "%Y-%m-%d %H:%M:%S")  # <class 'datetime.datetime'>
    # 遍历整个表：优化的方法（样例）
    WalkThroughTableSample()

    # # mongo转换mysql
    # mysql = MysqlTool()
    # from sentiment.mongo_tool import MongoTool
    # mongo = MongoTool()
    # docGen = mongo.MongoReadAllDoc(collection='com')
    # for doc in docGen:
    #     com = mysql.convertDocToComment(doc)
    #     mysql.insertOneDic(com)

