#!/usr/bin/env python
# coding: UTF-8

from tools.MysqlClient import MysqlClient
import os
import time
from pandas import DataFrame

"""
学校级别数据量太大，查询处理时间较长。所以这里遍历数据库，用日期变化趋势的逻辑，把数据处理为DataFrame，处理结果存入数据库表
GetJson模块直接查询
借助limit和自增序列主键id分表查询，查询到一块就处理，处理好将旧日期数据（若多条就是除最后一条，因为表中数据日期升序）写入
"""


class SchAc:
    def __init__(self):
        self.mc = MysqlClient()

    def mainfunc(self):
        colList = ['admin', 'sci', 'acad', 'dorm', 'sport', 'lib', 'med', 'none']
        df = DataFrame(columns=colList).astype(int)

        # 参数准备
        startID = 1
        batchCount = 10000
        while True:
            # 查询
            sql = "select acrec.ac_datetime, ac_loc.category " \
                  "from acrec, ac_loc " \
                  "where acrec.node_id = ac_loc.node_id " \
                  "and id >= %s limit %s " % (startID, batchCount)

            tStart = time.time()
            results = self.mc.query(sql)

            # 处理数据results
            # linedfList=[]
            for result in results:
                ac_datetime = result[0]
                category = result[1]

                lineDict = {}
                for col in colList:
                    lineDict[col] = 0 if col != category else 1
                df.loc[ac_datetime] = lineDict

            # 准备下一轮查询
            df.fillna(0, inplace=True)
            df = df.resample("D").sum()
            df.fillna(0, inplace=True)
            print(df)

            # 把最后一条之前的写入数据库，留下最后一条继续循环处理
            if df.shape[0] != 1:
                dfToWrite = df.iloc[:-1]
                df = df.iloc[-1:]
                from app.helpers import insertDataFrameToDBTable
                insertDataFrameToDBTable(dfToWrite, 'sch_ac_datetrend', self.mc)

            startID += batchCount
            if len(results) != batchCount:
                break

            tEnd = time.time()
            print(batchCount, " 行 ", tEnd - tStart)

        print(startID)
        print(df)

        os.system("pause")


if __name__ == "__main__":
    pj = SchAc()
    pj.mainfunc()
