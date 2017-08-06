#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_
from datetime import datetime

"""消费类型日期变化"""


def GetJson_ConDateTrend(userID, startDate, endDate, modeDate):
    """
    返回Json：消费类型日期变化
    :param userID: 卡号
    :param startDate: 限定数据起始日期
    :param endDate: 限定数据结束日期
    :param modeDate: 日期模式，决定数据按怎样的粒度合并
    :return json_response: Echarts格式字典{'axisLabels': , 'legendLabels': , 'seriesData': , 'statRows': }
    """
    sql = db.session.query(consumption.con_datetime, dev_loc.category, consumption.amount).filter(
        and_(consumption.user_id == userID,
             consumption.dev_id == device.dev_id,
             device.node_id == dev_loc.node_id)).order_by(consumption.con_datetime)

    if startDate:
        sql = sql.filter(
            and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))

    results = sql.all()

    if not results:
        return {'errMsg': u'没有找到记录。'}

    # 处理数据，返回一个DataFrame
    datetimeList = [result.con_datetime for result in results]
    categoryList = [result.category for result in results]
    valList = [result.amount for result in results]

    from app.functions.Pro_DateTrend import get_date_trend
    df, dfStat = get_date_trend(datetimeList, categoryList, valList, modeDate)

    # 把数据包装成Echarts需要的格式
    formatStrList = ['%Y-%m-%d', '%Y-%m']

    if int(modeDate) == 2:
        formatStr = formatStrList[1]
    else:
        formatStr = formatStrList[0]

    axisLabels = list(map(lambda x: x.strftime(formatStr), df.index.tolist()))

    seriesData = []
    for colName, col in df.items():
        data = list(map(lambda x: float(x), col.tolist()))
        seriesData.append({'name': colName, 'data': data})

    # 把只需要用表格显示的统计数据单独用字典列表返回
    statRows = []
    for dfIndex, dfRow in dfStat.iterrows():
        dfRowDict = dfRow.to_dict()  # Series转为字典

        # 把np的float64转成python的float
        for k, v in dfRowDict.items():
            dfRowDict[k] = float(v)

        dfRowDict["index"] = dfIndex  # 代表这条数据的索引，前端会用到"index" （耦合）
        statRows.append(dfRowDict)

    json_response = {'axisLabels': axisLabels, 'seriesData': seriesData, 'statRows': statRows}
    return json_response
