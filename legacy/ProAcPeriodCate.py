#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import time
from pandas import DataFrame
from numpy import isnan
from app import helpers
import copy
import types

"""时间分布趋势"""
class ACPeriodCate:
    def __init__(self, oriDate, oriValues):
        """
        :param oriDate: 日期标签数组
        :param oriValues: 与oriDate 对应的值数组
        """
        self.oriDate = oriDate
        self.oriValues = oriValues

    def get_date_trend(self, mode_date):
        """
        :param mode_date: 日期模式，合并到最短时间单位. 0-day, 1-week, 2-month, 3-Quarter. (default 2)
        """
        axisLabels = self.oriDate[:]
        pointVals = [{copy.deepcopy(oriValue): 1} for oriValue in self.oriValues]

        rule_mode = {'0': 'D', '1': 'W', '2': 'M', '3': 'Q'}

        df = DataFrame(pointVals, index=axisLabels)
        df = df.resample(rule_mode[str(mode_date)]).sum()
        df = df.fillna(0)

        """各项总和"""
        # cols_name = []
        # for name, col in df.iteritems():
        #     cols_name.append(name)
        # df['SUM'] = 0
        # for i in xrange(len(cols_name)):
        #     df['SUM'] += df[cols_name[i]]

        axisLabels = map(lambda x: x.strftime('%Y-%m-%d'), df.index.tolist())  # 从dataframe 中取出作为索引的日期标签成为队列
        seriesData = []
        legendLabels = []
        for colName, col in df.iteritems():
            legendLabels.append(colName)
            data = map(lambda x: 0.0 if isnan(x) else float(x), col.tolist())
            seriesData.append({'name': colName, 'data': data})

        json_dateTrend = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData}
        return json_dateTrend

    def get_time_distribution(self):
        dates = self.oriDate[:]
        values = [{copy.deepcopy(oriValue): 1} for oriValue in self.oriValues]

        # 生成时间点和时间标签队列
        periods = []
        axisLabels = []
        for i in xrange(24):
            periods.append(time(i))
            axisLabels.append(str(i) + u'点~' + str((i + 1) % 24) + u'点')

        # 时间点队列 -> 时间区间队列
        periodRanges = []
        for i in xrange(len(periods)):
            periodRange = [periods[i], periods[(i + 1) % len(periods)]]
            periodRanges.append(periodRange)

        lTimes = map(lambda d: d.time(), dates)  # Keep time
        vals = []     # Init vals
        for i in xrange(len(periods)):
            vals.append({})

        # Add to total vals
        for i in xrange(len(lTimes)):
            for j in xrange(len(periodRanges)):
                if periodRanges[j][0] <= lTimes[i] < periodRanges[j][1]:
                    vals[j + 1] = helpers.mergeDict(vals[j + 1], values[i])

        df = DataFrame(vals)

        seriesData = []
        legendLabels = []
        for colName, col in df.iteritems():
            legendLabels.append(colName)
            data = map(lambda x: 0 if isnan(x) else int(x), col.tolist())
            seriesData.append({'name': colName, 'data': data})

        json_timeDistribution = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData}
        return json_timeDistribution
