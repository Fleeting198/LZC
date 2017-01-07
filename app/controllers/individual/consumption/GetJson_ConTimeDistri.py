#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_
from numpy import isnan

"""消费时间分布，每天24小时的平均类型金额"""

def GetJson_ConTimeDistri(userID, startDate, endDate):
    """
    :param userID: 工号
    :param startDate: 限定数据起始日期
    :param endDate: 限定数据结束日期
    :return json_response: {'axisLabels': , 'legendLabels': , 'seriesData': }
    """
    # Query
    strQuery = db.session.query(consumption.con_datetime, dev_loc.category, consumption.amount).filter(
        and_(consumption.user_id == userID,
             consumption.dev_id == device.dev_id,
             device.node_id == dev_loc.node_id)).order_by(consumption.con_datetime)

    if startDate:
        strQuery = strQuery.filter(
            and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))

    results = strQuery.all()

    if not results:
        return {'errMsg': u'没有找到记录。'}

    # 处理数据，返回一个DataFrame
    dateList = [result.con_datetime for result in results]
    categoryList = [result.category for result in results]
    valList = [result.amount for result in results]

    from app.controllers.Pro_TimeDistr import get_time_distribution
    data = get_time_distribution(dateList, categoryList, valList)

    # 把数据包装成Echarts需要的格式
    axisLabels = []
    for i in xrange(24):
        axisLabels.append(str(i) + u'点~' + str((i + 1) % 24) + u'点')

    seriesData = []
    legendLabels = []
    for colName, col in data.iteritems():
        legendLabels.append(colName)
        data = map(lambda x: 0.0 if isnan(x) else float(x), col.tolist())
        seriesData.append({'name': colName, 'data': data})

    json_response = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData}
    return json_response