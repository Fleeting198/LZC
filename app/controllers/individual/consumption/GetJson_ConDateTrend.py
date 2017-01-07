#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_

"""消费类型日期变化"""


def GetJson_ConDateTrend(userID, startDate, endDate, modeDate):
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

    from app.controllers.Pro_DateTrend import get_date_trend
    df = get_date_trend(dateList, categoryList, valList, modeDate)

    # 把数据包装成Echarts需要的格式
    axisLabels = map(lambda x: x.strftime('%Y-%m-%d'), df.index.tolist())  # 从dataframe 中取出作为索引的日期标签成为队列
    seriesData = []
    legendLabels = []
    for colName, col in df.iteritems():
        legendLabels.append(colName)
        data = map(lambda x: float(x), col.tolist())
        seriesData.append({'name': colName, 'data': data})

    json_response = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData}
    return json_response
