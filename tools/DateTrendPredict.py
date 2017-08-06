#!/usr/bin/env python
# coding: UTF-8
from pandas import DataFrame, Series
from datetime import datetime, date, timedelta
import pandas as pd
from tools.MysqlClient import MysqlClient
from app.helpers import proper_ARIMA, insertDataFrameToDBTable
from statsmodels.tsa.arima_model import ARIMA
import logging

""" 从数据库中查询时间序列数据，构造成多列dataframe，对每一列进行滚动数据预测，存入数据库
"""


class DateTrendPredict:
    def __init__(self, datatype):
        self.mc = MysqlClient()
        self.targetTable = "sch_" + datatype + "_datetrend"
        self.minDate = "2015-01-01"
        self.predictLen = 60

        if datatype == 'ac':
            self.colList = ['med', 'dorm', 'acad', 'admin', 'sci', 'sport', 'lib', 'none']
        elif datatype == 'con':
            self.colList = ['food', 'shop', 'discipline', 'sport', 'water', 'study', 'med', 'none']
        else:
            raise ValueError

    def DateTrendPredict(self):
        # 构造查询语句
        sqlcol = ','.join(self.colList)
        sql = "select id_date, %s from %s where id_date >= '%s'" % (sqlcol, self.targetTable, self.minDate)
        results = self.mc.query(sql)  # 实施查询
        logging.info("Select source data from DB: %s" % sql)

        df = DataFrame(columns=self.colList)  # 初始化DataFrame

        # 将查询结果转变为DataFrame
        for result in results:
            id_date = result[0]
            # 数据库里时间是date，resample函数要求datetime，combine把date和time结合起来
            id_date = datetime.combine(id_date, datetime.min.time())

            lineDict = {}
            for i in range(len(self.colList)):
                lineDict[self.colList[i]] = float(result[i + 1])

            df.loc[id_date] = lineDict

        # 开始预测
        # 定义预测起止日期
        startDate = df[-1:].index[0]
        endDate = startDate + timedelta(self.predictLen)

        # 生成预测日期列表
        predictDateList = [startDate + timedelta(days=i) for i in range((endDate - startDate).days + 1)]

        allPredictionsList = []
        # 遍历列，分别预测
        for col in df.columns:
            logging.info("Start forecast %s" % col)
            history = pd.Series(df[col])[:]  # 原始时间序列
            predictions = Series(name=col)

            # 遍历预测日期列表
            hasModel = False
            p, q, aic = 0, 0, 0
            for t in predictDateList:
                # 构建ARIMA模型，以history为输入
                if hasModel:
                    logging.info("Using existed model: p: %d, q: %d, aic: %f" % (p, q, aic))
                    # 用第一次选出的参数构建模型
                    # 若参数报错，重选模型
                    try:
                        model_fit = ARIMA(history, order=(p, 2, q)).fit(disp=0, method='css')
                    except ValueError:
                        # 重选模型
                        logging.warning("Readapt ARIMA model")
                        model_fit, p, q, aic = proper_ARIMA(history, maxLag=9, diff=2)
                else:
                    # 自动选取合适参数
                    logging.info("First time adapt ARIMA model")
                    model_fit, p, q, aic = proper_ARIMA(history, maxLag=9, diff=2)
                    hasModel = True

                output = model_fit.forecast()[0][0]  # 预测1天
                history.loc[t] = output  # 添加预测结果到历史中，做滚动预测
                predictions.loc[t] = output  # 添加预测结果

            allPredictionsList.append(predictions)  # 记录该列预测结果到列表中

        # 用列表构造DataFrame，包含所有预测结果
        dfPredict = pd.concat(allPredictionsList, axis=1)

        logging.info("Start insert dataframe")
        insertDataFrameToDBTable(dfPredict, self.targetTable, self.mc)
        logging.info("End insert dataframe")


if __name__ == "__main__":
    pj = DateTrendPredict("ac")
    pj.DateTrendPredict()
    pj2 = DateTrendPredict("con")
    pj2.DateTrendPredict()
