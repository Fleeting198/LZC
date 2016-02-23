#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-16 Created -C
# 02-18 Weekly done.

from datetime import time, datetime, timedelta, date
import copy
import types
from collections import Counter


class DateTimeValueProcess():
    """
    输入坐标（日期，可重复）与对应值，对其进行统计。
    """
    oriDate = []  # 日期
    oriValues = []  # 与日期对应的  地点分类字符串

    def __init__(self, dates, vals=None):
        self.oriDate = dates
        self.oriValues = vals  # 若不传值列表则设次数为 1

    def dateTrend(self, modeDate=2):
        """
        日期趋势，输入日期模式，输出合并后的日期、节点值和累积值。
        默认日期模式为月
        """
        # Copy source data.
        axisLabels = self.oriDate[:]

        # 构造元素为dict的队列
        pointVals = []
        for i in range(len(axisLabels)):
            pointVals.append({copy.deepcopy(self.oriValues[i]): 1})

        # ========================

        axisLabels = map(lambda x: x.date(), axisLabels)  # Keep only date.

        # 补全没有记录的日期，值为0。
        # 遍历日期，若当前日期大于前一个日期超过1天，插入后一天日期。
        # 有插入的情况下
        i = 1
        while i < len(axisLabels):
            if axisLabels[i] - axisLabels[i - 1] > timedelta(days=1):
                axisLabels.insert(i, axisLabels[i - 1] + timedelta(days=1))
                pointVals.insert(i, {})  # 没有门禁记录的值
            else:
                i += 1

        # 日期降维。
        if modeDate == 0:
            pass
        elif modeDate == 2:
            axisLabels = map(lambda d: str(d)[:7], axisLabels)
        elif modeDate == 4:
            axisLabels = map(lambda d: str(d)[:4], axisLabels)
        elif modeDate == 1:
            # 遍历日期，转变为一周"起始年月日~结束月日"，date-weekday 就为周起始，date + 6-weekday为周结束。
            # datetime.weekday() 周一为0，周日为6
            axisLabels = map(lambda d: str(d - timedelta(d.weekday())) + ' ~ ' + (
            d + timedelta(days=6) - timedelta(d.weekday())).strftime(format='%m-%d'), axisLabels)
        elif modeDate == 3:
            pass

        # 遍历日期，合并相同日期以及对应的值
        i = 1
        while i < len(axisLabels):  # 每轮循环都要获取长度，用以遍历这个动态改变长度的列表
            if axisLabels[i] == axisLabels[i - 1]:
                # 去除 下标i-1  或i ?
                del axisLabels[i - 1]  # 去除日期

                # Counter 可能效率更低
                # pointVals[i] = dict(Counter(pointVals[i])+Counter(pointVals[i-1]))

                pointVals[i] = self.mergeDict(pointVals[i], pointVals[i-1])
                del pointVals[i - 1]  # 去除值

            else:
                i += 1

        axisLabels = map(lambda x: str(x), axisLabels)

        return axisLabels, pointVals


    def timeDistribution(self):
        """
        时间分布，输出各时间段总计数，目的在于对比。
        """
        # Copy source data.
        dates = self.oriDate[:]
        values = []
        for i in range(len(dates)):
            values.append({copy.deepcopy(self.oriValues[i]): 1})

        # Time periods：23~5 5~12 12~20 20~23
        period = (time(5), time(12), time(20), time(23))
        axisLabels = ('23点~5点', '5点~12点', '12点~20点', '20点~23点')
        lTimes = map(lambda d: d.time(), dates)  # Keep time.

        vals = []  # Init vals
        for i in range(len(period)):
            vals.append({})

        # Add to total vals.
        for i in range(len(lTimes)):
            if period[0] <= lTimes[i] < period[1]:
                vals[1] = self.mergeDict(vals[1], values[i])
            elif period[1] <= lTimes[i] < period[2]:
                vals[2] = self.mergeDict(vals[2], values[i])
            elif period[2] <= lTimes[i] < period[3]:
                vals[3] = self.mergeDict(vals[3], values[i])
            else:
                vals[0] = self.mergeDict(vals[0], values[i])

        return axisLabels, vals


    def mergeDict(self, dict1, dict2):
        """
        dict1 = dict1 + dict2
        合并相同的key的值
        """
        for k, v in dict2.iteritems():
            dict1[k] = dict1[k] + v if k in dict1 else 1
        return dict1
