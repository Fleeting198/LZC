#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pandas import DataFrame

"""
门禁日期分类访问总数趋势
消费日期分类访问总价趋势
"""

def get_date_trend(dateList, categoryList, valList, modeDate):
    """
    通过resample合并日期相同的访问量
    :param dateList: 日期列表
    :param categoryList: 与日期对应的访问类型，记一次访问
    :return df: DataFrame的形式，索引是日期，包含两列：门禁分类和访问数量
    """
    modeDate=int(modeDate)
    rule_mode = "DWMQ"  # 分别代表日、周、月、季度

    recordDictList=[]
    for i in xrange(len(categoryList)):
        recordDictList.append({categoryList[i]: valList[i]})

    df = DataFrame(recordDictList, index=dateList)
    df = df.resample(rule_mode[modeDate]).sum()
    df = df.fillna(0)
    # TODO: 数据类型从float64改成int

    return df