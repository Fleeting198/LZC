#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import LocalStrings as lstr
import sys, os
from statsmodels.tsa.arima_model import ARIMA
from pandas import DataFrame
from tools.MysqlClient import MysqlClient
import collections
from ProjectRootPath import getProjectDir
import pickle


def translate(ipt):
    """根据dict翻译字符串，若字典中不存在则返回原输入
    :param ipt: 要翻译的字符串
    """
    if ipt in lstr.dictTrans:
        return lstr.dictTrans[ipt]
    return ipt


def translateSeriesData(seriesData):
    for datum in seriesData:
        datum['name'] = translate(datum['name'])


def translateStatRows(statRows):
    for datum in statRows:
        datumKeys = list(datum.keys())
        for key in datumKeys:
            val = datum[key]
            del datum[key]
            nkey = translate(key)
            val = translate(val)
            datum[nkey] = val


def mergeDict(dict1, dict2):
    """dict1 = dict1 + dict2  合并相同的key的值
    :param dict1: 第一个用以合并的字典
    :param dict2: 第二个用以合并的字典
    """
    for k, v in dict2.items():
        dict1[k] = dict1[k] + v if k in dict1 else 1
    return dict1


def proper_ARIMA(data_ts, maxLag=6, diff=1):
    init_aic = sys.maxsize
    init_p = 0
    init_q = 0
    init_properModel = None
    for p in range(maxLag):
        for q in range(maxLag):
            model = ARIMA(data_ts, order=(p, diff, q))
            try:
                results_ARIMA = model.fit(disp=0, method='css')
            except:
                continue
            aic = results_ARIMA.aic
            if aic < init_aic:
                init_p = p
                init_q = q
                init_properModel = results_ARIMA
                init_aic = aic
    return init_properModel, init_p, init_q, init_aic


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
        for k, v in dfRowDict.items():
            listcols.append(str(k))
            listvalues.append(str(v))

        strcols = ",".join(listcols)
        strvalues = ",".join(listvalues)
        sql = "insert ignore into %s (%s) values (%s)" % (tableName, strcols, strvalues)

        try:
            mysqlclient.query(sql)
        except:
            print(sql)
            mysqlclient.rollback()

    mysqlclient.commit()


def insertDataFrameToDBTable2(df, tableName, mysqlclient):
    # 把df写入数据库
    tableName = str(tableName)

    for dfIndex, dfRow in df.iterrows():
        listcols = []
        listvalues = []

        dfRowDict = dfRow.to_dict()  # Series转为字典
        for k, v in dfRowDict.items():
            # print str(k), str(v)
            listcols.append(str(k))
            listvalues.append(str(v))

        strcols = ",".join(listcols)
        strvalues = ",".join(listvalues)
        sql = "insert ignore into %s (%s) values (%s)" % (tableName, strcols, strvalues)
        try:
            mysqlclient.query(sql)
        except:
            print(sql)
            mysqlclient.rollback()

    mysqlclient.commit()


def updatePrefs(**kwargs):
    path = getProjectDir()
    path += '\\ProjectPrefs.pkl'

    if os.path.exists(path):
        try:
            with open(path, 'rb') as f:
                prefs = pickle.load(f)
        except:
            prefs = {}
    else:
        prefs = {}
    prefs.update(kwargs)
    print(prefs)
    with open(path, 'wb') as f:
        pickle.dump(prefs, f)


def IQRHighLowLimit(li):
    """
    去除异常值
    数理统计中通过四分位点定义的IQR，上下限为[75% + 1.6*IQR，25% - 1.6*IQR]
    """
    if not isinstance(li, list):
        raise ValueError
    l = li[:]
    l.sort()
    lenL = len(l)
    q1 = l[int(lenL * 0.25)]
    q3 = l[int(lenL * 0.75)]
    IQR2 = (q3 - q1) * 1.6
    lowLimit = q1 - IQR2
    highLimit = q3 + IQR2
    return lowLimit, highLimit
