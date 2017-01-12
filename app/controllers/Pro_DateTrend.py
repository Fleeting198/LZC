#!/usr/bin/env python
# coding: UTF-8

from pandas import DataFrame


"""
日期趋势的数据处理，用于消费和门禁的处理
"""


def get_date_trend(datetimeList, categoryList, valList, modeDate):
    """
    通过resample合并日期相同的访问量
    :param datetimeList: 日期列表
    :param categoryList: 与日期对应的访问类型，记一次访问
    :param valList: 值列表，门禁是1，消费是金额
    :param modeDate: 数据粒度选项，0日、1周、2月、3季度
    :return df: DataFrame的形式，索引是日期，列是存在的门禁和消费分类，内容是合并量
    :return dfStat: DataFrame，df的统计信息
    """

    modeDate = int(modeDate)
    rule_mode = "DWMQ"  # 分别代表日、周、月、季度
    recordDictList = []
    for i in xrange(len(categoryList)):
        recordDictList.append({categoryList[i]: valList[i]})

    df = DataFrame(recordDictList, index=datetimeList, dtype=float)
    df.fillna(0,inplace=True)

    # 先按天统计再预测
    df = df.resample("D").sum()

    df = df.resample(rule_mode[modeDate]).sum()
    print df

    # 获取统计信息
    dfStat=df.describe()
    dfStat.drop('count', inplace=True)

    return df,dfStat
