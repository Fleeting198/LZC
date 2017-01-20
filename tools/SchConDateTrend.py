#!/usr/bin/env python
# coding: UTF-8

from MysqlClient import MysqlClient
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
        colList = ['food', 'shop', 'discipline', 'recharge', 'sport', 'water', 'study', 'med', 'none']
        df = DataFrame(columns=colList)

        # 参数准备
        startID = 0
        batchCount = 10000
        while True:
            # 查询
            sql = "select consumption.con_datetime, dev_loc.category, consumption.amount " \
                  "from consumption, device, dev_loc " \
                  "where consumption.dev_id = device.dev_id and dev_loc.node_id = device.node_id " \
                  "and id >= %s limit %s " % (str(startID), str(batchCount))

            tStart = time.time()

            results = self.mc.query(sql)

            # 处理数据results
            for result in results:
                con_datetime = result[0]
                category = result[1]
                amount = float(result[2])

                # 添加df行
                td = {}
                for col in colList:
                    td[col] = 0.0 if col != category else amount
                df.loc[con_datetime] = td

            # 准备下一轮查询
            df.fillna(0, inplace=True)
            df = df.resample("D").sum()
            df.fillna(0, inplace=True)
            print df

            # 把最后一条之前的写入数据库，留下最后一条继续循环处理
            if df.shape[0] != 1:
                dfToWrite = df.iloc[:-1]
                df = df.iloc[-1:]

                from app.helpers import insertDataFrameToDBTable
                insertDataFrameToDBTable(dfToWrite, 'sch_con_datetrend', self.mc)

            startID += batchCount
            if len(results) != batchCount:
                break

            tEnd = time.time()
            print batchCount, " 行 ", tEnd - tStart

        print startID

        os.system("pause")


if __name__ == "__main__":
    pj = SchAc()
    pj.mainfunc()
