#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 02-11 Built by 陈骏杰
#   输入：日期和对应消费增量，日期模式。
#   输出：符合对应模式的日期、连续总计支出（初始量0 + 增量）、节点支出
#
#   模式：日0，周1，月2，季3，年4。
#   完成了日、月、年，未做周、季。

from datetime import time
import types


class Expenditure():
    dates = []  # 日期
    amounts = []  # 与日期对应的消费额

    def __init__(self, dates, amounts):
        self.dates = dates
        self.amounts = amounts

    def dateTrend(self, modeDate):
        """
        日期趋势，输入日期模式，输出合并后的日期、节点值和累积值。
        """
        # Copy source data.
        axisLables = self.dates[:]
        accumulatedVals = self.amounts[:]

        # 日期降维，仅用字符串切片处理年、月。
        if modeDate == 0:
            axisLables = map(lambda d: d.date(), axisLables)
        elif modeDate == 2:
            axisLables = map(lambda d: str(d.date())[:7], axisLables)
        elif modeDate == 4:
            axisLables = map(lambda d: str(d.date())[:4], axisLables)

        i = 1
        while i < len(axisLables):  # 每轮循环都要获取长度
            # 取当前和前一个记录的日期（天）
            # 若日期相同，合并日期和对应增量
            if axisLables[i] == axisLables[i - 1]:
                axisLables = axisLables[:i - 1] + axisLables[i:]  # 日期去除
                accumulatedVals[i] += accumulatedVals[i - 1]  # 增量合并
                accumulatedVals = accumulatedVals[:i - 1] + accumulatedVals[i:]  # 增量去除
            else:
                i += 1

        # 保存节点值
        pointVals = accumulatedVals[:]
        # 累加连续值
        for i in range(1, len(accumulatedVals)):
            accumulatedVals[i] += accumulatedVals[i - 1]

        # Make sure type.
        axisLables = map(lambda x: str(x), axisLables)
        accumulatedVals = map(lambda x: float(x), accumulatedVals)
        pointVals = map(lambda x: float(x), pointVals)

        return axisLables, accumulatedVals, pointVals

    def timeDistribution(self):
        """
        时间分布，输出各时间段总计数，目的在于对比。
        """
        # Copy source data.
        lDates = self.dates[:]
        lAmounts = self.amounts[:]

        print type(lAmounts[1])

        # Time periods：
        # 23~5 5~12 12~20 20~23
        period = (time(5), time(12), time(20), time(23))
        axisLables = ('23点~5点', '5点~12点', '12点~20点', '20点~23点')

        # Init vals
        vals = []
        for i in range(len(period)):
            vals[i] = float(0)

        lTimes = map(lambda d: d.time(), lDates)  # Keep time.

        # lDates = map(lambda d: d.date(), lDates)
        # len_mdates = len(list(set(lDates)))  # Day count to divide.

        # Add to total vals.
        for i in range(len(lTimes)):
            if period[0] <= lTimes[i] < period[1]:
                vals[1] += lAmounts[i]
            elif period[1] <= lTimes[i] < period[2]:
                vals[2] += lAmounts[i]
            elif period[2] <= lTimes[i] < period[3]:
                vals[3] += lAmounts[i]
            else:
                vals[0] += lAmounts[i]

        for i in range(len(vals)):
            # vals[i] = vals[i] / len_mdates if len_mdates != 0 else 0
            vals[i] = round(vals[i], 2)

        return axisLables, vals
