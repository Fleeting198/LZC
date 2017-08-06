#!/usr/bin/env python
# coding: UTF-8
from tools.MysqlClient import MysqlClient
from tools.ProcessRecorder import ProcessRecorder
from datetime import datetime
import traceback
from tools.Apriori_ToL2 import apriori_to_L2
from app.helpers import updatePrefs

"""
基于关联计算的人际关系
遍历数据库，选取时间相同相近的所有门禁记录，查询到内存
困难：时间相近的重复处理
解决：用时间和地点生成唯一标识符(hash)；不看时间相近，把时间粒度放粗到分钟级别就算时间相同的。
    记录上一次统计的{地点：事务}字典，对当前时间统计时，若地点键在上一次记录中，上一时间记录合并这一次的，这一时间的保持不变，当移到下一个时间时，将原来的上一次时间记录处理
困难：不知道内存够不够，得先试一试

按相同的地点，把卡号放在同一个事务中
困难：事务的存储结构，dataframe，index事务编号TID，columns卡号

对这些事务队列用Apriori算法，定义支持度阈值，算到L2，停止
L1和L2存入文本文件

遍历时间范围内的数据（项目中是所有数据），对于新的L1，L2的每项，到存储文件中查找是否已有数据，若无新增；若有提取，计算平均值再存入

全部记录遍历完成后，计算置信度，

字典：{项集：支持度，...}
"""


class RelationShip:
    def __init__(self, tableNameDataSource):
        self.mc = MysqlClient()
        self.tableNameDataSource = tableNameDataSource
        self.tableNameRelationConfData = 'ac_relation_confData'
        self.tableNameRelationSuppData = 'ac_relation_suppData'
        self.totalNum = self.mc.query('select count(*) from %s' % self.tableNameDataSource)[0][0]
        self.pr = ProcessRecorder(processName="RelationShip_" + self.tableNameDataSource[:3],
                                  localDataSet={'suppData': {}, 'startID': 1, 'copy_last_dict_loc_user': {},
                                                'currDate': '2001-01-01'},
                                  total=self.totalNum,
                                  warningMessage='Calculating RelationShip of %s' % self.tableNameDataSource)

    def caculateSuppData(self):
        """
        计算支持度，返回支持度字典
        """

        def add_to_dict(row, last_dict_loc_user, cur_dict_loc_user):
            """加入当前字典，合并到上一个时间字典（若有）"""
            user_id = str(row[1])
            node_id = int(row[2])

            if node_id in cur_dict_loc_user:
                cur_dict_loc_user[node_id].append(user_id)
            else:
                cur_dict_loc_user[node_id] = [user_id]

            if node_id in last_dict_loc_user:
                last_dict_loc_user[node_id].append(user_id)

        # 遍历获取门禁记录
        batchSize = 10000
        # 因为上一时间的字典在处理时会改变，所以切换下一个时间时备份（不断点续传的话没用）
        last_dict_loc_user = self.pr.localDataSet['copy_last_dict_loc_user']
        cur_dict_loc_user = {}
        currDate = datetime.strptime(self.pr.localDataSet['currDate'], '%Y-%m-%d')
        tmpSuppData = {}
        cntTransactionsRelation = 0

        try:
            while 1:
                sql = "select ac_datetime, user_id, node_id from acrec " \
                      "where id >= %s limit %s" % (self.pr.localDataSet['startID'], batchSize)
                rows = self.mc.query_one(sql)
                batchCount = 0

                for row in rows:
                    batchCount += 1
                    ac_datatime = row[0]
                    ac_datatime = ac_datatime.replace(second=0)

                    # 新的时间小于等于1分钟 或 刚开始处理
                    if (ac_datatime - currDate).seconds >= 60:
                        # 更新当前时间
                        currDate = ac_datatime
                        self.pr.localDataSet['currDate'] = currDate.strftime('%Y-%m-%d')

                        # 当前dict_loc_user中key为TID，对应列表为事务项集，调用模块计算频繁项集
                        tmpSuppData = apriori_to_L2(last_dict_loc_user.values())

                        # 对suppData中每一条，到字典中查找，若有累加，若无添加
                        for k, v in tmpSuppData.items():
                            if k in self.pr.localDataSet['suppData']:
                                self.pr.localDataSet['suppData'][k] += v
                            else:
                                self.pr.localDataSet['suppData'][k] = v

                        # 累加last_dict_loc_user中元素个数
                        cntTransactionsRelation += len(last_dict_loc_user)

                        last_dict_loc_user = cur_dict_loc_user
                        self.pr.localDataSet['copy_last_dict_loc_user'] = last_dict_loc_user
                        cur_dict_loc_user = {}  # 清空

                    add_to_dict(row, last_dict_loc_user, cur_dict_loc_user)

                # 准备下一轮循环查询，或者跳出循环
                self.pr.add(batchSize)
                self.pr.localDataSet['startID'] += batchSize

                if batchCount < batchSize: break

        except:
            # store the current process
            print('\nProcess stopped when processing %s' % self.pr.localDataSet['currDate'])
            self.pr.store_process()
            traceback.print_exc()

        # 循环结束处理完成，这里的支持度是次数不是频率，保存事务数量，之后处理
        # pickle 保存 cntTransactionsRelation
        print("cntTransactionsRelation = ", cntTransactionsRelation)
        updatePrefs(cntTransactionsRelation=cntTransactionsRelation)

        # 把suppData写入数据库
        return self.pr.localDataSet['suppData']

    def insertSuppDataIntoDB(self, suppData):
        """
        插入支持度数据到数据库
        :param suppData: 支持度
        """
        listToInsert = []
        for k, v in suppData.items():
            k = list(k)
            listToInsert.append((k, v))

        sql = 'insert ignore into ' + self.tableNameRelationSuppData + ' (itemSet,supportCount) values ("%s",%s)'
        self.mc.execute_many(sql, listToInsert)
        self.mc.commit()

    def selectSuppDataFromDB(self):
        sql = "select itemSet,supportCount from " + self.tableNameRelationSuppData
        results = self.mc.query_one(sql)
        suppDataSingle, suppDataDouble = {}, {}
        for result in results:
            itemSet = eval(result[0])
            supportRate = float(result[1])

            # 字符串是两个元素的元组时转过来是元组，包含一个元素的元组转过来是那一个元素
            if len(itemSet) == 2:
                suppDataDouble[itemSet] = supportRate
            else:
                suppDataSingle[itemSet] = supportRate
        return suppDataSingle, suppDataDouble

    def calculateConfData(self, suppDataSingle, suppDataDouble, minConf=0.1):
        """
        生成关联规则
        :param suppDataSingle: 长度1 支持度
        :param suppDataDouble: 长度2 支持度
        :param confData: 关联规则
        """

        def writeConfData(l, r):
            if l not in confData:
                confData[l] = {}

            pLeft = suppDataSingle[l]
            confidence = float(suppRate) / pLeft
            if confidence < minConf: return False
            confData[l][r] = confidence
            return True

        confData = {}
        for itemSet, suppRate in suppDataDouble.items():
            itemSet = list(itemSet)
            writeConfData(itemSet[0], itemSet[1])
            writeConfData(itemSet[1], itemSet[0])

        return confData

    def insertConfDataIntoDB(self, confData, suppDataDouble):
        """
        插入关联规则到数据库
        :param confData: 关联规则
        :param suppDataDouble: 为了将支持度一起写入数据库
        """
        dataToInsert = []
        for K, V in confData.items():
            for k, v in V.items():
                pkey1 = (K, k)
                pkey2 = (k, K)
                if pkey1 in suppDataDouble:
                    suppCount = suppDataDouble[pkey1]
                elif pkey2 in suppDataDouble:
                    suppCount = suppDataDouble[pkey2]
                else:
                    raise ValueError('2人关系不存在')
                dataToInsert.append((K, k, v, suppCount))

        sql = 'insert into  ' + self.tableNameRelationConfData + ' (left_user_id, right_user_id, confRate, suppCount) ' \
                                                                 'values ("%s", "%s", %s, %s)'

        for d in dataToInsert:
            try:
                self.mc.query(sql % d)
            except:
                continue

        # pymysql.err.DataError: (1406, "Data too long for column 'left_user_id' at row 1")
        # self.mc.execute_many(sql,dataToInsert)

        self.mc.commit()


if __name__ == '__main__':
    ts = RelationShip("acrec")

    suppData = ts.caculateSuppData()
    print('SuppData complete')

    print('Start to insert SuppData')
    ts.insertSuppDataIntoDB(suppData)
    print('SuppData insert complete')

    suppDataS, suppDataD = ts.selectSuppDataFromDB()
    print('SuppData select complete')

    confData = ts.calculateConfData(suppDataS, suppDataD, minConf=0)
    print('ConfData complete')

    ts.insertConfDataIntoDB(confData, suppDataD)
    print('ConfData insert complete')
