#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import time
from pandas import DataFrame
from numpy import isnan
import copy
import types


def ACPeriodCate(oriDate, oriValues, mode_date):
    """
    :param oriDate: 日期标签数组
    :param oriValues: 与oriDate 对应的值数组
    :param mode_date: 日期模式，合并到最短时间单位. 0-day, 1-week, 2-month, 3-Quarter. (default 2)
    """

    # =====================================================
    # dateTrend
    # =====================================================

    # Copy source data.
    axisLabels = oriDate[:]
    pointVals = [{copy.deepcopy(oriValue): 1} for oriValue in oriValues]

    rule_mode = {'0': 'D', '1': 'W', '2': 'M', '3': 'Q'}

    df = DataFrame(pointVals, index=axisLabels)
    df = df.resample(rule_mode[str(mode_date)], how='sum')
    df = df.fillna(0)

    cols_name = []
    for name, col in df.iteritems():
        cols_name.append(name)
    df['SUM'] = 0
    for i in range(len(cols_name)):
        df['SUM'] += df[cols_name[i]]

    df['PER_DORM'] = df['dorm']/df['SUM'] if 'dorm' in df else 0  # 仅当存在宿舍值时才计算宿舍比重，否则设为0
    axisLabels = map(lambda x: x.strftime('%Y-%m-%d'), df.index.tolist())  # 从dataframe 中取出作为索引的日期标签成为队列
    seriesData = []
    legendLabels = []
    for colName, col in df.iteritems():
        legendLabels.append(colName)
        data = map(lambda x: 0.0 if isnan(x) else float(x), col.tolist())
        seriesData.append({'name': colName, 'data': data})

    json_dateTrend = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData}

    # =====================================================
    # timeDistribution
    # =====================================================

    # Copy source data.
    dates = oriDate[:]
    values = [{copy.deepcopy(oriValue): 1} for oriValue in oriValues]

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

    lTimes = map(lambda d: d.time(), dates)  # Keep time.
    vals = []  # Init vals
    for i in range(len(periods)):
        vals.append({})

    # Add to total vals.
    for i in range(len(lTimes)):
        for j in range(len(periodRanges)):
            if periodRanges[j][0] <= lTimes[i] < periodRanges[j][1]:
                vals[j + 1] = mergeDict(vals[j + 1], values[i])

    df = DataFrame(vals)
    # print df

    seriesData = []
    legendLabels = []
    for colName, col in df.iteritems():
        legendLabels.append(colName)
        data = map(lambda x: 0 if isnan(x) else int(x), col.tolist())
        seriesData.append({'name': colName, 'data': data})

    json_timeDistribution = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData}

    return json_dateTrend, json_timeDistribution


def mergeDict(dict1, dict2):
    """dict1 = dict1 + dict2  合并相同的key的值
    :param dict1: 第一个用以合并的字典
    :param dict2: 第二个用以合并的字典
    """
    for k, v in dict2.iteritems():
        dict1[k] = dict1[k] + v if k in dict1 else 1
    return dict1
