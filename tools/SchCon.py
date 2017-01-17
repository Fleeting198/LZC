#!/usr/bin/env python
# coding: UTF-8

from MysqlClient import MysqlClient
import os
import time
import traceback
from pandas import DataFrame
import pandas as pd


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
            # linedfList=[]
            for result in results:
                con_datetime = result[0]
                category = result[1]
                amount = float(result[2])

                # linedf = DataFrame({category: amount}, index=[con_datetime], columns=colList)
                # linedf.fillna(0, inplace=True)
                # linedfList.append(linedf)
                td = {}
                for col in colList:
                    td[col] = 0.0 if col != category else amount
                df.loc[con_datetime] = td

            # df = pd.concat(linedfList)

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
