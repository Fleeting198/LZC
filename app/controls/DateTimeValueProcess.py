#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-16 Created -C
# 02-18 Weekly done.

from datetime import time, datetime, timedelta, date
import types


class DateTimeValueProcess():
    """
    输入坐标（日期，可重复）与对应值，对其进行统计。
    """
    oriDate = []  # 日期
    oriValues = []  # 与日期对应的消费额

    def __init__(self, dates, vals=None):
        self.oriDate = dates
        self.oriValues = [1] * len(dates) if vals is None else vals  # 若不传值列表则设次数为 1

    def dateTrend(self, modeDate=2):
        """
        日期趋势，输入日期模式，输出合并后的日期、节点值和累积值。
        默认日期模式为月
        """
        # Copy source data.
        axisLabels = self.oriDate[:]
        accumulatedVals = self.oriValues[:]

        # Keep only date.
        axisLabels = map(lambda x: x.date(), axisLabels)

        # 补全没有记录的日期，值为0。
        # 遍历日期，若当前日期大于前一个日期超过1天，插入后一天日期。
        # 有插入的情况下
        i = 1
        while i < len(axisLabels):
            if axisLabels[i] - axisLabels[i - 1] > timedelta(days=1):
                axisLabels.insert(i, axisLabels[i - 1] + timedelta(days=1))
                accumulatedVals.insert(i, 0)
            else:
                i += 1

        # 日期降维。
        # TODO: 日级别数据处理返回是否必要，流量消耗太大。
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
        # TODO: 生成按季度分的数据，考虑到交互性可能由前端JS负责？
        elif modeDate == 3:
            pass

        # 遍历日期，合并相同日期以及对应的值
        i = 1
        while i < len(axisLabels):  # 每轮循环都要获取长度，用以遍历这个动态改变长度的列表
            if axisLabels[i] == axisLabels[i - 1]:
                # 去除 下标i-1  或i ?
                del axisLabels[i - 1]  # 去除日期
                accumulatedVals[i] += accumulatedVals[i - 1]  # 合并值
                del accumulatedVals[i - 1]  # 去除值

                # axisLabels = axisLabels[:i - 1] + axisLabels[i:]
                # accumulatedVals = accumulatedVals[:i - 1] + accumulatedVals[i:]
            else:
                i += 1

        # 保存节点值
        pointVals = accumulatedVals[:]
        # 累加连续值
        for i in range(1, len(accumulatedVals)):
            accumulatedVals[i] += accumulatedVals[i - 1]

        # Make sure type.
        axisLabels = map(lambda x: str(x), axisLabels)
        accumulatedVals = map(lambda x: float(x), accumulatedVals)
        pointVals = map(lambda x: float(x), pointVals)

        return axisLabels, accumulatedVals, pointVals

    def timeDistribution(self):
        """
        时间分布，输出各时间段总计数，目的在于对比。
        """
        # Copy source data.
        dates = self.oriDate[:]
        values = map(lambda x: float(x), self.oriValues)

        # 生成时间点和时间标签队列。
        periods=[]
        axisLabels=[]
        for i in range(24):
            periods.append(time(i))
            axisLabels.append(str(i)+u'点~'+str((i + 1) % 24)+u'点')

        # 时间点队列 -> 时间区间队列。
        periodRanges = []
        for i in range(len(periods)):
            periodRange = [periods[i], periods[(i+1)%len(periods)]]
            periodRanges.append(periodRange)

        vals = [float(0)] * len(periods)  # Init vals
        lTimes = map(lambda d: d.time(), dates)  # Keep time.

        # dates = map(lambda d: d.date(), dates)
        # len_mdates = len(list(set(dates)))  # Day count to divide.

        # Add to total vals.
        for i in range(len(lTimes)):
            for j in range(len(periodRanges)):
                if periodRanges[j][0] <= lTimes[i] < periodRanges[j][1]:
                    vals[j+1] += values[i]

            # Old version.
            # if periods[0] <= lTimes[i] < periods[1]:
            #     vals[1] += values[i]
            # elif periods[1] <= lTimes[i] < periods[2]:
            #     vals[2] += values[i]
            # elif periods[2] <= lTimes[i] < periods[3]:
            #     vals[3] += values[i]
            # else:
            #     vals[0] += values[i]

        for i in range(len(vals)):
            # vals[i] = vals[i] / len_mdates if len_mdates != 0 else 0
            vals[i] = round(vals[i], 2)

        return axisLabels, vals