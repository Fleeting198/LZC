#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import helpers
from datetime import time, datetime, timedelta, date
from pandas import Series, DataFrame
from numpy import isnan
import copy
import types


def ACPeriodCate(res_datetimes, res_categorys, mode_date):
    # Format return data for ECharts setting.

    # dateTrend  ===============================
    oriDate = res_datetimes
    oriValues = res_categorys

    # Copy source data.
    axisLabels = oriDate[:]
    pointVals = [{copy.deepcopy(oriValue): 1} for oriValue in oriValues]

    rule_mode = {'0': '1D', '1': '1W', '2': '1M', '3': '1Q', '4': '1Y'}

    df = DataFrame(pointVals, index=axisLabels)
    df = df.resample(rule_mode[str(mode_date)], how='sum')

    axisLabels = map(lambda x: x.strftime('%Y-%m-%d'), df.index.tolist())

    seriesData = []
    legendLabels = []
    for colName, col in df.iteritems():
        legendLabels.append(colName)
        data = map(lambda x: 0.0 if isnan(x) else x, col.tolist())
        seriesData.append({'name': colName, 'data': data})

    json_dateTrend = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData}

    # timeDistribution   ===============================
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

    seriesData = []
    legendLabels = []
    for colName, col in df.iteritems():
        legendLabels.append(colName)
        data = map(lambda x: 0.0 if isnan(x) else x, col.tolist())
        seriesData.append({'name': colName, 'data': data})

    json_timeDistribution = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData}

    return json_dateTrend, json_timeDistribution


def mergeDict(dict1, dict2):
    """
    dict1 = dict1 + dict2
    合并相同的key的值
    :param dict2:
    :param dict1:
    """
    for k, v in dict2.iteritems():
        dict1[k] = dict1[k] + v if k in dict1 else 1
    return dict1
