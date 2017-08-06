#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pandas import DataFrame

"""门禁时间分布"""


def get_time_distribution(dateList, categoryList, valList):
    """
    :param dateList: 日期列表
    :param categoryList: 与日期对应的访问类型，记一次访问
    :param valList: 对应的访问记录的值，门禁是1次，消费是金额
    :return df: DataFrame
    """
    recordDictList = []
    for i in range(len(categoryList)):
        recordDictList.append({categoryList[i]: valList[i]})

    df = DataFrame(recordDictList, index=dateList)
    df.fillna(0, inplace=True)

    numDays = len(df.resample('D').sum())  # 按天合并后获取df行数，即取样时间范围天数

    lines = []
    for i in range(24):
        line = df[df.index.hour == i].sum()
        line /= numDays
        lines.append(line)

    df = DataFrame(lines, index=range(24))
    dfStat = df.describe()
    dfStat.drop('count', inplace=True)

    return df, dfStat
