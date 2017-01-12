#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_

"""门禁时间分布，每天24小时的平均门禁分类次数"""


def GetJson_AcTimeDistri(userID, startDate, endDate):
    """
    返回Json：门禁趋势与分布
    :param userID: 工号
    :param startDate: 限定数据起始日期
    :param endDate: 限定数据结束日期
    """
    # Query
    strQuery = db.session.query(acrec.ac_datetime, ac_loc.category).filter(
        and_(acrec.user_id == userID, acrec.node_id == ac_loc.node_id)).order_by(acrec.ac_datetime)

    if startDate:
        strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))

    results = strQuery.all()
    if not results:
        return {'errMsg': u'没有找到记录。'}

    dateList = [result.ac_datetime for result in results]
    categoryList = [result.category for result in results]
    valList = [1] * len(categoryList)

    from app.controllers.Pro_TimeDistr import get_time_distribution
    df, dfStat = get_time_distribution(dateList, categoryList, valList)

    # 把数据包装成Echarts需要的格式
    axisLabels = []
    for i in xrange(24):
        axisLabels.append(str(i) + u'点~' + str((i + 1) % 24) + u'点')

    seriesData = []
    legendLabels = []
    for colName, col in df.iteritems():
        legendLabels.append(colName)
        df = map(lambda x: float(x), col.tolist())
        seriesData.append({'name': colName, 'data': df})

    # 把只需要用表格显示的统计数据单独用字典列表返回
    statRows = []
    for dfIndex, dfRow in dfStat.iterrows():
        dfRowDict = dfRow.to_dict()  # Series转为字典

        # 把np的float64转成python的float
        for k, v in dfRowDict.iteritems():
            dfRowDict[k] = float(v)

        dfRowDict["index"] = dfIndex  # 代表这条数据的索引，前端会用到"index" （耦合）
        statRows.append(dfRowDict)

    json_response = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData,
                     'statRows': statRows}
    return json_response
