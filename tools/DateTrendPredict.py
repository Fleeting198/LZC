#!/usr/bin/env python
# coding: UTF-8
from pandas import DataFrame, Series
from datetime import datetime, date, timedelta
import pandas as pd
from tools.MysqlClient import MysqlClient
from app.helpers import proper_ARIMA, insertDataFrameToDBTable
from statsmodels.tsa.arima_model import ARIMA


class DateTrendPredict():
    def __init__(self):
        self.mc = MysqlClient()
        self.colListAc = [ 'med','dorm', 'acad', 'admin', 'sci', 'sport', 'lib', 'none']
        self.colListCon = ['food', 'shop', 'discipline', 'sport', 'water', 'study', 'med', 'none']

    def mainfunc(self, datatype):
        # 查询
        if datatype == 'con':
            colList = self.colListCon
        elif datatype == 'ac':
            colList = self.colListAc
        else:
            raise ValueError

        sqlcol = ','.join(colList)

        sql = "select id_date," + sqlcol + " from sch_" + datatype + "_datetrend"
        results = self.mc.query(sql)

        df = DataFrame(columns=colList)

        # 获得DataFrame
        for result in results:
            id_date = result[0]

            # 只要2015年的数据
            min_date = date(2015, 1, 1)
            if id_date < min_date:
                continue

            # 数据库里时间是date，resample要datetime，combine把date和time结合起来
            id_date = datetime.combine(id_date, datetime.min.time())

            lineDict = {}
            for i in xrange(len(colList)):
                lineDict[colList[i]] = float(result[i + 1])

            df.loc[id_date] = lineDict

        # 开始预测
        # 定义预测起止日期
        startDate = df[-1:].index[0]
        predictLen = 50
        endDate = startDate + timedelta(predictLen)
        predictDateList = [startDate + timedelta(days=i) for i in range((endDate - startDate).days + 1)]
        # startDate = startDate.strftime("%Y-%m-%d")
        # endDate = endDate.strftime("%Y-%m-%d")

        allPredictionsList = []
        for col in df.columns:
            print "start forecast %s" % col
            ts = pd.Series(df[col])  # 原始时间序列
            history = ts[:]
            predictions = Series(name=col)

            # 省点时间，一个序列的滚动预测中参数不变
            hasModel = False
            p = 0
            q = 0
            for t in predictDateList:
                if not hasModel:
                    model_fit, p, q, bic = proper_ARIMA(history, maxLag=9, diff=2)
                    print p, q
                    hasModel = True
                else:
                    model_fit = ARIMA(history, order=(p, 2, q)).fit(disp=0, method='css')

                output = model_fit.forecast()
                yhat = output[0][0]
                predictions.loc[t] = yhat
                history.loc[t] = yhat
            allPredictionsList.append(predictions)

        dfPredict = pd.concat(allPredictionsList, axis=1)
        print dfPredict

        insertDataFrameToDBTable(dfPredict, "sch_" + datatype + "_datetrend", self.mc)


if __name__ == "__main__":
    pj = DateTrendPredict()
    # pj.mainfunc("con")
    pj.mainfunc("ac")
