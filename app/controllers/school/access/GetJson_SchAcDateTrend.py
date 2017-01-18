#!/usr/bin/env python
# coding: UTF-8

from app.models import *
from datetime import date


def GetJson_SchAcDateTrend(modeDate):
    modeDate = int(modeDate)
    strQuery = db.session.query(sch_ac_datetrend).order_by(sch_ac_datetrend.id_date)
    results = strQuery.all()

    if not results:
        return {'errMsg': u'没有找到记录。'}

    colList = ['dorm', 'acad', 'admin', 'sci', 'sport', 'lib', 'med', 'none']

    datePredictStart = date(2016, 1, 1)
    idPredictStart = 0
    for i in xrange(len(results)):
        if results[i].id_date >= datePredictStart:
            idPredictStart = i
            break

    resultsOrigin = results[:idPredictStart]
    resultsPredict = results[idPredictStart:]

    from app.controllers.Pro_DateTrendPredict import Pro_DateTrendPredict
    df, dfStat, dfPredict, dfPredictStat = Pro_DateTrendPredict(resultsOrigin, resultsPredict, modeDate, colList)

    axisLabels, legendLabels, seriesData, statRows = packDateTrendToEchartsForm(df, dfStat, modeDate)
    json_origin = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData,
                   'statRows': statRows}

    axisLabels, legendLabels, seriesData, statRows = packDateTrendToEchartsForm(dfPredict, dfPredictStat, modeDate)
    json_predict = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData,
                    'statRows': statRows}

    json_response = {'json_origin': json_origin, 'json_predict': json_predict}
    return json_response

def packDateTrendToEchartsForm(df, dfStat, modeDate):
    # 把数据包装成Echarts需要的格式
    formatStrList = ['%Y-%m-%d', '%Y-%m']
    if modeDate == 2:
        formatStr = formatStrList[1]
    else:
        formatStr = formatStrList[0]
    axisLabels = map(lambda x: x.strftime(formatStr), df.index.tolist())

    seriesData = []
    legendLabels = []
    for colName, col in df.iteritems():
        legendLabels.append(colName)
        data = map(lambda x: float(x), col.tolist())
        seriesData.append({'name': colName, 'data': data})


    # 把只需要用表格显示的统计数据单独用字典列表返回
    statRows = []
    for dfIndex, dfRow in dfStat.iterrows():
        dfRowDict = dfRow.to_dict()  # Series转为字典

        # 把np的float64转成python的float
        for k, v in dfRowDict.iteritems():
            dfRowDict[k] = float(v)

        dfRowDict["index"] = dfIndex  # 代表这条数据的索引，前端会用到"index" （耦合）
        statRows.append(dfRowDict)

    return axisLabels, legendLabels, seriesData, statRows
