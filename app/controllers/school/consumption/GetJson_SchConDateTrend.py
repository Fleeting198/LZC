#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from datetime import date


def GetJson_SchConDateTrend(modeDate):
    modeDate = int(modeDate)
    strQuery = db.session.query(sch_con_datetrend).order_by(sch_con_datetrend.id_date)
    results = strQuery.all()

    if not results:
        return {'errMsg': u'没有找到记录。'}

    colList = ['food', 'shop', 'discipline', 'sport', 'water', 'study', 'med', 'none']

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

    from app.helpers import packDataToEchartsForm
    axisLabels, legendLabels, seriesData, statRows = packDataToEchartsForm(df, dfStat, modeDate)
    json_origin = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData,
                   'statRows': statRows}

    axisLabels, legendLabels, seriesData, statRows = packDataToEchartsForm(dfPredict, dfPredictStat, modeDate)
    json_predict = {'axisLabels': axisLabels, 'legendLabels': legendLabels, 'seriesData': seriesData,
                    'statRows': statRows}

    json_response = {'json_origin': json_origin, 'json_predict': json_predict}
    return json_response
