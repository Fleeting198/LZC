#!/usr/bin/env python
# coding: UTF-8

from pandas import DataFrame
import pandas as pd
from decimal import Decimal
import datetime
import sys
import MySQLdb
from MysqlClient import MysqlClient, get_data_from_source

"""
每条消费：日期、金额、类型，选一年数据
统计：
消费额度：
每月各大类消费总量
每月各大类消费总次数
月列表累加，各大类统计期一年总消费量和消费次数
不分消费类时，每月消费量、次数；全年消费量、次数

消费强度：
每月平均每次消费额，每月各大类平均每次消费额
"""


class PovertyJudge:
    def __init__(self):
        self.mc = MysqlClient()
        self.avg_vals = 0
        self.avg_times = 0
        self.avg_per = 0

    def JudgeOne(self, datetimeList, categoryList, valList):
        """
        计算一个人的消费总额、消费次数、消费强度，强度=总额/次数，所以只返回总额和次数
        :param datetimeList:
        :param categoryList:
        :param valList:
        :return sum_vals:
        :return sum_times:
        """
        recordDictList = []
        for i in xrange(len(categoryList)):
            recordDictList.append({categoryList[i]: valList[i], 'times_' + categoryList[i]: 1})

        df = DataFrame(recordDictList, index=datetimeList, dtype='float')
        df = df.resample("M").sum()  # 按月统计
        df.fillna(0, inplace=True)

        # 以下通过df循环列完成每月金额总和、次数总和、各类消费强度计算
        colNames = list(df.columns)
        df['sum_vals'] = df['sum_times'] = 0
        for colName in colNames:
            if colName[:6] == 'times_':
                df['sum_times'] += df[colName]
            else:
                df['sum_vals'] += df[colName]
                df['per_' + colName] = df[colName] / df['times_' + colName]

        # 总消费强度
        df['per_total'] = df['sum_vals'] / df['sum_times']

        # 统计时间段（一年）金额总和、次数总和
        df.loc['sum'] = df.sum()
        # print df

        sum_vals = df.loc['sum', 'sum_vals']
        sum_times = df.loc['sum', 'sum_times']
        per_total = sum_vals / sum_times

        # print sum_vals,sum_times,per_total

        return sum_vals, sum_times

    def updateOne(self, userID):
        results = self.mc.query("select con_datetime, dev_loc.category, amount "
                                "from consumption, dev_loc, device "
                                "where consumption.user_id = '%s' and consumption.dev_id = device.dev_id and device.node_id = dev_loc.node_id" % userID)
        if not results:
            return

        datetimeList = [result[0] for result in results]
        categoryList = [result[1] for result in results]
        valList = [result[2] for result in results]

        sum_vals, sum_times = self.JudgeOne(datetimeList, categoryList, valList)
        sum_per = sum_vals / sum_times

        if sum_vals:
            self.avg_vals = (self.avg_vals + sum_vals) / 2
        if sum_times:
            self.avg_times = (self.avg_times + sum_times) / 2
        if sum_per:
            self.avg_per = (self.avg_per + sum_per) / 2

        try:
            self.mc.query("update individual "
                          "set con_sum_vals = %f ,con_sum_times = %d "
                          "where user_id = '%s'" % (sum_vals, sum_times, userID))
            self.mc.commit()
        except:
            self.mc.rollback()

    def updateAll(self):
        self.mc._cursor.execute("select user_id from individual")
        c = 0
        for row in self.mc._cursor:
            if not row:
                break

            c += 1
            print "%d / 79146" % c
            self.updateOne(row[0])

    def updateIndicator(self):
        if self.avg_vals == 0 or self.avg_times == 0 or self.avg_per == 0:
            self.getAvg()

        print self.avg_vals, self.avg_times, self.avg_per

        c=0
        self.mc._cursor.execute("select user_id, con_sum_vals, con_sum_times from individual")
        for row in self.mc._cursor:
            if not row:
                break

            userID = row[0]
            sum_vals = row[1]
            sum_times = row[2]

            if sum_vals is None or sum_times is None or sum_vals == 0 or sum_times == 0:
                continue

            c+=1
            print "%d / 79146"%c

            sum_per = sum_vals / sum_times

            index_vals = (sum_vals - self.avg_vals) / sum_vals
            index_times = (sum_times - self.avg_times) / sum_times
            index_per = (sum_per - self.avg_per) / sum_per

            try:
                self.mc.query("update individual "
                              "set index_vals = %f ,index_times = %f, index_per = %f "
                              "where user_id = '%s'" % (index_vals, index_times, index_per, userID))
                self.mc.commit()
            except:
                self.mc.rollback()

    def getAvg(self):
        self.mc._cursor.execute("select con_sum_vals, con_sum_times from individual")
        for row in self.mc._cursor:
            if not row:
                break

            sum_vals = row[0]
            sum_times = row[1]

            if sum_vals is None or sum_times is None:
                continue

            sum_per = sum_vals / sum_times

            if sum_vals:
                self.avg_vals = (self.avg_vals + sum_vals) / 2
            if sum_times:
                self.avg_times = (self.avg_times + sum_times) / 2
            if sum_per:
                self.avg_per = (self.avg_per + sum_per) / 2


if __name__ == "__main__":
    pj = PovertyJudge()
    pj.updateIndicator()
