#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pandas import Series
from decimal import *
import types


class DateTimeValueProcess:
    """输入坐标（日期，可重复）与对应值，对其进行统计。
    """
    def __init__(self, dates, vals=None):
        self.oriDate = dates  # 日期
        self.oriValues = [1] * len(dates) if vals is None else vals  # 与日期对应的消费额， 若不传值列表则设次数为 1

    def get_date_trend(self, mode_date=2):
        """日期趋势，输入日期模式，输出合并后的日期、节点值和累积值。
        :param mode_date: 日期模式，合并到最短时间单位. 0-day, 1-week, 2-month, 3-Quarter. (default 2)
        """
        # TODO: 日期坐标字符串调整
        ts = Series(self.oriValues, index=self.oriDate)

        rule_mode = {'0': 'D', '1': 'W', '2': 'M', '3': 'Q'}
        # 按照modeDate 合并数据
        ts = ts.resample(rule_mode[str(mode_date)], how='sum')

        axisLabels = map(lambda x: x.strftime('%Y-%m-%d'), ts.index.tolist())
        pointVals = map(lambda x: round(float(x), 2), ts.values.tolist())
        accumulatedVals = pointVals[:]
        for i in range(1, len(accumulatedVals)):
            accumulatedVals[i] = round(accumulatedVals[i] + accumulatedVals[i - 1], 2)

        return axisLabels, accumulatedVals, pointVals

    def get_time_distribution(self, mode_time=1):
        """时间分布，输出各时间段总计数，目的在于对比。
        :param mode_time: period for time distribution. 0-day, 1-week, 2-month. (default 1)
        """
        dates = self.oriDate[:]
        values = self.oriValues[:]

        span_d = (dates[-1] - dates[0]).days
        span_w = float((dates[-1] - dates[0]).days) / 7
        span_y = float((dates[-1] - dates[0]).days) / 365

        periods = []
        axisLabels = []
        if mode_time == 0:
            # 按天 - 24小时分割时间段
            dates = map(lambda x: x.time().hour, dates)
            for i in range(24):
                periods.append(i)
                axisLabels.append(str(i) + u'点~' + str((i + 1) % 24) + u'点')
            # 跨多少天
            divider = Decimal(span_d)

        elif mode_time == 1:
            # 按周 - 7天分割时间段
            dates = map(lambda x: x.weekday()+1, dates)
            axisLabels = [u'周一',u'周二',u'周三', u'周四',u'周五', u'周六',u'周日',]
            periods = [1,2,3,4,5,6,7]
            # 跨多少周
            divider = Decimal(span_w)

        elif mode_time == 2:
            # 按年 - 月分割时间段
            dates = map(lambda x: x.day, dates)
            axisLabels = [u'一月', u'二月', u'三月', u'四月', u'五月', u'六月', u'七月', u'八月', u'九月', u'十月', u'十一月', u'十二月',]
            periods = range(1,13)
            # 跨多少年
            divider = Decimal(span_y)

        vals = [Decimal(0)] * len(periods)  # Init vals

        dividers = [0]*len(periods) # 用以取平均值的除数
        for i in range(len(dates)):
            for j in range(len(periods)):
                if dates[i] == periods[j]:
                    dividers[j] += 1
                    vals[j] += values[i]

        # vals 取平均值
        # 求日期跨度
        for i in range(len(vals)):
            vals[i] = vals[i]/divider if divider!= 0 else 0

        vals = map(lambda x:float(x), vals)
        return axisLabels, vals
