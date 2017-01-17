#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import LocalStrings as lstr
import sys
from statsmodels.tsa.arima_model import ARIMA
import traceback
from pandas import DataFrame
from tools.MysqlClient import MysqlClient


def translate(ipt):
    """根据dict翻译字符串，若字典中不存在则返回原输入
    :param ipt: 要翻译的字符串
    """
    if isinstance(ipt, basestring) and ipt in lstr.dictTrans:
        return lstr.dictTrans[ipt]
    return ipt


def mergeDict(dict1, dict2):
    """dict1 = dict1 + dict2  合并相同的key的值
    :param dict1: 第一个用以合并的字典
    :param dict2: 第二个用以合并的字典
    """
    for k, v in dict2.iteritems():
        dict1[k] = dict1[k] + v if k in dict1 else 1
    return dict1


def proper_ARIMA(data_ts, maxLag=6, diff=1):
    init_bic = sys.maxint
    init_p = 0
    init_q = 0
    init_properModel = None
    for p in xrange(maxLag):
        for q in xrange(maxLag):
            model = ARIMA(data_ts, order=(p, diff, q))
            try:
                results_ARMA = model.fit(disp=0, method='css')
            except:
                continue
            bic = results_ARMA.bic
            if bic < init_bic:
                init_p = p
                init_q = q
                init_properModel = results_ARMA
                init_bic = bic
    return init_properModel, init_p, init_q, init_bic


def insertDataFrameToDBTable(df, tableName, mysqlclient):
    # 把df写入数据库

    if not isinstance(df, DataFrame):
        raise ValueError
    if not isinstance(mysqlclient, MysqlClient):
        raise ValueError
    tableName = str(tableName)

    for dfIndex, dfRow in df.iterrows():
        listcols = ['id_date']
        listvalues = ["'" + dfIndex.to_pydatetime().strftime("%y-%m-%d") + "'"]

        dfRowDict = dfRow.to_dict()  # Series转为字典
        for k, v in dfRowDict.iteritems():
            # print str(k), str(v)
            listcols.append(str(k))
            listvalues.append(str(v))

        strcols = ",".join(listcols)
        strvalues = ",".join(listvalues)
        sql = "insert into %s (%s) values (%s)" % (tableName, strcols, strvalues)

        try:
            mysqlclient.query(sql)
        except:
            print sql
            print traceback.format_exc()
            mysqlclient.rollback()
        else:
            mysqlclient.commit()


def packDataToEchartsForm(df, dfStat, modeDate):
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
