#!/usr/bin/env python
# coding: UTF-8

from pandas import DataFrame
from datetime import datetime


def Pro_DateTrendPredict(resultsOrigin, resultsPredict, modeDate, colList):
    modeDate = int(modeDate)
    rule_mode = "DWMQ"  # 分别代表日、周、月、季度

    def resultsToDataFrame(results):
        df=DataFrame(columns=colList)
        for result in results:
            lineDict = {}
            for col in colList:
                lineDict[col] = float(getattr(result, col))

            id_date=result.id_date
            id_date=datetime.combine(id_date,datetime.min.time())

            df.loc[id_date]=lineDict
        return df

    df = resultsToDataFrame(resultsOrigin)
    dfPredict = resultsToDataFrame(resultsPredict)

    df = df.resample(rule_mode[modeDate]).sum()
    dfPredict = dfPredict.resample(rule_mode[modeDate]).sum()

    # 获取统计信息
    dfStat = df.describe()
    dfStat.drop('count', inplace=True)

    dfPredictStat = dfPredict.describe()
    dfPredictStat.drop('count', inplace=True)

    return df, dfStat, dfPredict, dfPredictStat
