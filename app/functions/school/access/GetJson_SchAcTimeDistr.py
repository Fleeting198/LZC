#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from pandas import DataFrame

"""学校全部数据门禁时间分布，每天24小时的平均门禁分类次数"""


def GetJson_SchAcTimeDistr():
    # Query
    dbQuery = sch_ac_timedistr.query
    results = dbQuery.all()

    colList = ['dorm', 'acad', 'admin', 'sci', 'sport', 'lib', 'med', 'none']
    # 将数据库数据转化为df
    df = DataFrame(columns=colList)
    for result in results:
        lineDict = {}
        for col in colList:
            lineDict[col] = float(getattr(result, col))
        id_time = result.id_time
        df.loc[id_time] = lineDict

    dfStat = df.describe()
    dfStat.drop('count', inplace=True)

    # 把数据包装成Echarts需要的格式
    axisLabels = []
    for i in range(24):
        axisLabels.append(str(i) + u'点~' + str((i + 1) % 24) + u'点')

    seriesData = []
    for colName, col in df.items():
        df = list(map(lambda x: float(x), col.tolist()))
        seriesData.append({'name': colName, 'data': df})

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
