#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-16 Created -C
# 02-18 Weekly done.
# 02-24 Pandas imported.

from datetime import time
from pandas import Series
import types


class DateTimeValueProcess:
    """
    输入坐标（日期，可重复）与对应值，对其进行统计。
    """
    def __init__(self, dates, vals=None):
        self.oriDate = dates  # 日期
        self.oriValues = [1] * len(dates) if vals is None else vals  # 与日期对应的消费额， 若不传值列表则设次数为 1

    def get_date_trend(self, mode_date=2):
        """
        日期趋势，输入日期模式，输出合并后的日期、节点值和累积值。
        默认日期模式为月
        """
        # TODO: 日期坐标字符串调整

        ts = Series(self.oriValues, index=self.oriDate)

        rule_mode = {'0': '1D', '1': '1W', '2': '1M', '3': '1Q', '4': '1Y'}
        # 按照modeDate 合并数据
        ts = ts.resample(rule_mode[str(mode_date)], how='sum')

        axisLabels = map(lambda x: x.strftime('%Y-%m-%d'), ts.index.tolist())
        pointVals = map(lambda x: round(float(x), 2), ts.values.tolist())
        accumulatedVals = pointVals[:]
        for i in range(1, len(accumulatedVals)):
            accumulatedVals[i] = round(accumulatedVals[i] + accumulatedVals[i - 1], 2)

        return axisLabels, accumulatedVals, pointVals

    def get_time_distribution(self):
        """
        时间分布，输出各时间段总计数，目的在于对比。
        """
        # Copy source data.
        dates = self.oriDate[:]
        values = map(lambda x: float(x), self.oriValues)

        # 生成时间点和时间标签队列。
        periods = []
        axisLabels = []
        for i in range(24):
            periods.append(time(i))
            axisLabels.append(str(i) + u'点~' + str((i + 1) % 24) + u'点')

        # 时间点队列 -> 时间区间队列。
        periodRanges = []
        for i in range(len(periods)):
            periodRange = [periods[i], periods[(i + 1) % len(periods)]]
            periodRanges.append(periodRange)

        vals = [float(0)] * len(periods)  # Init vals
        lTimes = map(lambda d: d.time(), dates)  # Keep time.

        # dates = map(lambda d: d.date(), dates)
        # len_mdates = len(list(set(dates)))  # Day count to divide.

        # Add to total vals.
        for i in range(len(lTimes)):
            for j in range(len(periodRanges)):
                if periodRanges[j][0] <= lTimes[i] < periodRanges[j][1]:
                    vals[j + 1] += values[i]

        for i in range(len(vals)):
            # vals[i] = vals[i] / len_mdates if len_mdates != 0 else 0
            vals[i] = round(vals[i], 2)

        return axisLabels, vals